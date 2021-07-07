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

from .models import Item_Info , Item_Stock
from .serializers import ItemSerializer, PriceSerializer, ValueSerializer

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
        except :
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
        default_storage.save("img" + '/' + file_name, file)
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
2. shoppingcart_api
    - request : ID, 수량 , 총 결제 금액 받음 
    - do : 재고 테이블 갱신
    - reponse : ID, 수량 , 총 결제 금액
'''
@api_view(['GET', 'PUT', 'POST','DELETE'])
def shopping_cart_api(request,id):
    try:
        item = Item_Info.objects.get(pid=id)
        
    except Item_Info.DoesNotExist:
        
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item)

        # 둘 중 하나 고르기
        return Response(serializer.data, status=200)
        #return Response(json.dumps({"status": 200, "data":serializer.data}))
        
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = ItemSerializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

