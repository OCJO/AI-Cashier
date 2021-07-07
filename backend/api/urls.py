from django.conf.urls import url, include
from django.urls import path, include
from .views import shopping_cart_api, object_detect_api
from django.views.generic import TemplateView

urlpatterns = [

    path("shopping/<str:id>", shopping_cart_api, name="shopping_cart"),
    path("object_detect/", object_detect_api, name="object_detect"),
]
