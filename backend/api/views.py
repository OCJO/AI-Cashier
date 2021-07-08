from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os
import json

import uuid
import datetime

from .models import Item_Info , Item_Stock
from .serializers import ItemSerializer,  ValueSerializer

'''
1. ObjectDetectAPI
    - request : 이미지 파일
    - do : 이미지 파일 저장 / ai 모델 load  
    - reponse : 결과 이미지 path / 상품 정보들 / 상태코드    
'''
@api_view(['POST'])
def object_detect_api(request):

    if request.method == 'POST':
        try:
            file = request.FILES['image']
            print("잘넘어왔음")
        except KeyError as e :
            print('예외가 발생했음', e)
            # for key in request.FILES.keys():
            #     print(key)
            # for key, value in request.FILES.items():
            #     print(key, value)
            print("파일이 안넘어왔어")
            return Response(status=status.HTTP_404_NOT_FOUND)

        print("파일 잘 넘어왔음")
        file_name = str(uuid.uuid4())
        
        # front에서 파일 받은 후 저장 
        default_storage.save("before_img" + '/' + file_name, file)
        file_url = "frontend/public/before_img/"+file_name+".jpg"

        '''
        ai 모델 
        -> ai 모델에 경로(file_url), 저장될 이름(file_name) 넣어주기. 
        =>[반환 값] : 1.결과 이미지 url / 2.결과 클래스 리스트
        '''

        # 아래 3 줄 실제로 할 필요 x -> ai 모델안에서 하고 반환해줌. 
        default_storage.save("img" + '/' + file_name + '.jpg', file)
        file_url = "img/"+file_name+".jpg"
        result_list = [0, 1, 1]
        result_dict={}
        for x in result_list:
            if x not in result_dict:
                result_dict[x]=1
            else:
                result_dict[x]+=1
        print("====result_dict====")
        print(result_dict)
        data_dict=[]
        # Item_Info
        for key,value in result_dict.items():
            item = Item_Info.objects.get(pid=key)
            serializer = ItemSerializer(item)
            
            json_data= serializer.data
            print(json_data)
            print("key,value=",key,value)
            json_data["value"]=value
            data_dict.append(json_data)

        print("=====dict====")
        print(data_dict)
        print("======result_data=====")
        result_data = {"path":file_url, "result":data_dict, "status":200}
        print(result_data)
    
    return Response(json.dumps(result_data))
    # 예시: {'path': 'img/6c7236c2-35a1-406d-9921-1b3b58de1a7f.jpg', 'result': [{'pid': '0', 'name': 'pepsi', 'price': 1500, 'value': 1}, {'pid': '1', 'name': 'coke', 'price': 3444, 'value': 1}], 'status': 200}

'''  
2. payment_api
    - request : ID, 수량 , 총 결제 금액 받음 
    - do : 재고 테이블 갱신
    - reponse : ID, 수량 , 총 결제 금액
'''

@api_view(['POST'])
def payment_api(request):

    if request.method == 'POST':
        # post 받는 형식대로 추후 추정
        try:
            _pid = request.POST['pid']
            _value = request.POST['value']
            _total_price = request.POST['total_price']
        except :
            print("값들이 안 넘어옴")
            return Response(status=status.HTTP_404_NOT_FOUND)

        print("_pid",_pid)
        print("_value",_value)
        print("_total_price",_total_price)

        # 가 데이터
        _pid = [0,1]
        _value = [3,4]
        _total_price = 5600

        # 재고 테이블 갱신
        for i in range(len(_pid)):
            this_id=_pid[i]
            this_value=_value[i]
            _stock_table = Item_Stock.objects.get(pid=this_id)
            _stock_table.value = _stock_table.value-this_value
            now=datetime.datetime.now()
            _stock_table.modify_date = now.strftime('%Y-%m-%d') # 2021-07-07
            _stock_table.save()

        result_dict={}
        result_dict["pid"]=_pid
        result_dict["value"]=_value
        result_dict["total_price"]=_total_price

        return Response(json.dumps(result_dict) , status=status.HTTP_201_CREATED)


 