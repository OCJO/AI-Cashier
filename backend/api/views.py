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
API
----- 
1. ObjectDetectAPI
    - do : 이미지 파일 저장 / ai 모델 load  
    - reponse : 결과 이미지 path / 상품 정보들 / 상태코드  
2. ShoppingCartAPI
    - do : ID, 수량 , 총 결제 금액 받음 / 재고 테이블 갱신
    - reponse : ID, 수량 , 총 결제 금액
'''

@api_view(['POST'])
def ObjectDetectAPI(request):
    try:
        file = request.FILES['image']
    except :
        
        return Response(status=status.HTTP_404_NOT_FOUND)

    file_name = str(uuid.uuid4())
    default_storage.save("img" + '/' + file_name, file)

    file_url = "img/"+file_name+".jpg"
    
    # 가데이터 - 실제 : ai 인식 후 결과 
    ai_result = [{
    "pid": "id02",
    "category_L": 1,
    "name": "can_coke",
    "price": 1000
    },{
    "pid": "id02",
    "category_L": 1,
    "name": "can_coke",
    "price": 1000
    },{
    "pid": "id02",
    "category_L": 1,
    "name": "can_coke",
    "price": 1000
    }]
    
    result_data = {"path":file_url, "result":ai_result, "status":200}

    
    return Response(result_data)
    

@api_view(['GET', 'PUT', 'POST','DELETE'])
def ShoppingCartAPI(request,id):
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

# GET 127.0.0.1:8000/api/hello/ 에 요청보내면 hello world print 하는 api임
@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")


@api_view(['GET'])
def ItemAPI(request, id):
    this_item = Item_Info.objects.get(pid=id)
    serializer = ItemSerializer(this_item)
    return Response(serializer.data)
# => pid=id01에 대해 리턴된 Response: {'pid': id01, 'category_L': 0, 'name': 'can_pepsi', 'value': 5, 'price': 1500}


@api_view(['GET'])
def PriceAPI(request, id):
    this_item = Item_Info.objects.get(pid=id)
    serializer = PriceSerializer(this_item)
    return Response(serializer.data)
# => pid=id01에 대해 리턴된 Response: {'pid': id01,  'price': 1500}

# update
class UpdateAPI(UpdateAPIView):

    queryset = Item_Info.objects.all()
        
    serializer_class = ValueSerializer

# delete
class DeleteAPI(DestroyAPIView):

    queryset = Item_Info.objects.all()
        
    serializer_class = ItemSerializer

# class view 로직
class LogicView(APIView):
    
    def get(self, request, format=None):
        item = Item_Info.objects.all()
        serializer = serializers.PriceSerializer(item, many=True)

        return Response(data=serializer.data)
# 사용하려면 api/urls.py에 아래 코드 추가해야함
'''
from .views import LogicView

urlpatterns = [
    url(r'^Logic/$', LogicView.as_view(), name='Logic'),
]
'''

# 리액트 프론트 연결 api - 사용 안함
class ReactAppView(View):
    
    def get(self, request):
        try:
            with open(os.path.join(str(settings.ROOT_DIR),
                                    'frontend',
                                    'build',
                                    'index.html')) as file:
                print("error 안남")
                return HttpResponse(file.read())

        except:
            print("error 남")
            return HttpResponse(status=501,)
# 참고 : https://jwlee010523.tistory.com/entry/%EC%9E%A5%EA%B3%A0%EC%99%80-%EB%A6%AC%EC%95%A1%ED%8A%B8-%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0-1?category=847381