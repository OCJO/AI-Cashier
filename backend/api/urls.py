from django.conf.urls import url, include
from django.urls import path, include
from .views import payment_api, object_detect_api
from django.views.generic import TemplateView

urlpatterns = [

    path("object_detect/", object_detect_api, name="object_detect"),
    path("payment/", payment_api, name="payment"),

]
