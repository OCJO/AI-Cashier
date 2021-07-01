from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os

from .models import Item_Info
from .serializers import ItemSerializer, PriceSerializer, ValueSerializer

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

# view 로직
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

# 리액트 프론트 연결 api
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