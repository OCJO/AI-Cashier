from django.conf.urls import url, include
from django.urls import path, include
from .views import payment_api, object_detect_api
from django.views.generic import TemplateView

urlpatterns = [
    
    # 이미지 인식 버튼 - 결과 이미지 전송
    path("object_detect/", object_detect_api, name="object_detect"),

    # 결제하기 버튼 - 재고 테이블 갱신
    path("payment/", payment_api, name="payment"),

]
