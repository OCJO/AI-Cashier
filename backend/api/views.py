from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from config.settings import yolo
from django.core.files.storage import default_storage
import os
import json
import cv2

import uuid
import datetime

from .models import Item_Info, Item_Stock
from .serializers import AllItemSerializer, ItemSerializer,  ValueSerializer

'''
1. object_detect_api
    [post]
    - request : 이미지 파일
    - do : 이미지 파일 저장 / ai 모델 load  
    - reponse : 결과 이미지 path / 상품 정보들 / 상태코드    
'''


@api_view(['POST'])
def object_detect_api(request):

    if request.method == 'POST':
        try:
            file = request.FILES['image']
            print("잘 넘어옴")
        except KeyError as e:
            print('예외가 발생 : ', e)
            # for key in request.FILES.keys():
            #     print(key)
            # for key, value in request.FILES.items():
            #     print(key, value)
            return Response(status=status.HTTP_404_NOT_FOUND)

        file_name = str(uuid.uuid4())

        # front에서 파일 받은 후 저장
        default_storage.save("before_img" + '/' + file_name+".jpg", file)
        test_file_url = "../frontend/public/before_img/"+file_name+".jpg"
        output_url = "../frontend/public/img/"+file_name+".jpg"
        # for frontend
        result_file_url = "img/"+file_name+".jpg"

        '''
        ai 모델 
        -> ai 모델에 경로(test_file_url), 저장될 이름(file_name) 넣어주기. 
        =>[반환 값] : 1.결과 이미지 url / 2.결과 클래스 리스트
        '''

        # '이미지 경로' 를 넣으면 OD 바운딩 박스가 그려진 이미지 데이터와 검출된 객체의 정보를 return

        image_imshow, result_list = yolo.object_detection(
            test_file_url, output_url)  # 테스트 이미지의 하위 경로와 위에 있는 파일이름
        print("인식결과 : ", result_list)

        # 처리한 이미지 저장
        #cv2.imshow("../frontend/public/img", image_imshow)
        #cv2.waitKey(0)

        result_dict = {}
        for x in result_list:
            if x not in result_dict:
                result_dict[x] = 1
            else:
                result_dict[x] += 1

        print("====result_dict====")
        print(result_dict)

        data_dict = []
        # Item_Info
        for key, value in result_dict.items():
            item = Item_Info.objects.get(pid=key)
            serializer = ItemSerializer(item)

            json_data = serializer.data
            json_data["value"] = value
            data_dict.append(json_data)

        print("======result_data=====")
        result_data = {"path": result_file_url,
                       "result": data_dict, "status": 200}
        print(result_data)

    return Response(json.dumps(result_data))
    # 예시: {'path': 'img/6c7236c2-35a1-406d-9921-1b3b58de1a7f.jpg', 'result': [{'pid': '0', 'name': 'pepsi', 'price': 1500, 'value': 1}, {'pid': '1', 'name': 'coke', 'price': 3444, 'value': 1}], 'status': 200}


'''
2. add_item_api
    [get]  
    - reponse : 대분류(category_L) 마다의 name, id / 상태코드  
    [post]
    - request : id
    - do : id에 해당하는 가격 가져옴
    - reponse : 가격  
'''


@api_view(['GET', 'POST'])
def add_item_api(request):

    if request.method == 'GET':

        data_dict = {}
        # 대분류 카테고리
        large_category = ['캔음료', '페트음료', '컵라면', '봉지과자', '아이스크림']

        # '대분류' 별 '소분류 정보(name:id)' 저장
        for idx in range(len(large_category)):
            data_dict[large_category[idx]] = add_small_category(idx)

        print("======result_data=====")
        result_data = {"result": data_dict, "status": 200}
        print(result_data)
        return Response(json.dumps(result_data))

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            _pid = data["pid"]
            
            print("try - request값", request.POST)
            print(_pid)
            print(type(_pid))
        except:
            print("except - request값", request.POST)
            print("값이 안넘어옴")
            return Response(status=status.HTTP_404_NOT_FOUND)
        print("넘어온 pid 값 : ", _pid)

        item = Item_Info.objects.get(pid=_pid)
        serializer = ItemSerializer(item)
        json_data = serializer.data
        price_ = json_data["price"]

        result_data = {"price": price_, "status": 200}
        print(result_data)
        return Response(json.dumps(result_data))

# 소분류 저장 / add_item_api 내에서 사용


def add_small_category(id):

    item = Item_Info.objects.filter(category_L=id)
    serializer = AllItemSerializer(item, many=True)

    json_data = serializer.data

    dict_ = {}
    for data in json_data:
        pid_ = data["pid"]
        name_ = data["name"]
        dict_[name_] = pid_  # key : name , value : id

    return dict_


'''  
3.. payment_api
    - request : ID, 수량 , 총 결제 금액 받음 
    - do : 재고 테이블 갱신
    - reponse : ID, 수량 , 총 결제 금액
'''


@api_view(['POST'])
def payment_api(request):

    # {"pid" : [0, 1], "id" : [3, 4], "total_price" : 5000}
    if request.method == 'POST':
        # post 받는 형식대로 추후 추정
        try:
            _pid = request.POST['pid']
            _value = request.POST['value']
            _total_price = request.POST['total_price']
        except:
            print("값들이 안 넘어옴")
            return Response(status=status.HTTP_404_NOT_FOUND)

        print("_pid", _pid)
        print("_value", _value)
        print("_total_price", _total_price)

        # 가 데이터
        _pid = [0, 1]
        _value = [3, 4]
        _total_price = 5600

        # 재고 테이블 갱신
        for i in range(len(_pid)):
            this_id = _pid[i]
            this_value = _value[i]
            _stock_table = Item_Stock.objects.get(pid=this_id)
            _stock_table.value = _stock_table.value-this_value
            now = datetime.datetime.now()
            _stock_table.modify_date = now.strftime('%Y-%m-%d')  # 2021-07-07
            _stock_table.save()

        result_dict = {}
        result_dict["pid"] = _pid
        result_dict["value"] = _value
        result_dict["total_price"] = _total_price

        return Response(json.dumps(result_dict), status=status.HTTP_201_CREATED)