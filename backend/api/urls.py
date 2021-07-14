from django.conf.urls import url, include
from django.urls import path, include
from .views import payment_api, object_detect_api, add_item_api
from django.views.generic import TemplateView

urlpatterns = [

    # 이미지 인식 버튼 - 결과 이미지 전송
    path("object_detect/", object_detect_api, name="object_detect"),

    # 항목추가 버튼 - 대,소분류 선택 / 가격 전송
    path("add_item/", add_item_api, name="add_item_api"),

    # 결제하기 버튼 - 재고 테이블 갱신
    path("payment/", payment_api, name="payment"),

]
