from django.urls import path, include
from .views import ReactAppView, HelloAPI, ItemAPI, PriceAPI, UpdateAPI, DeleteAPI

urlpatterns = [
    path("", ReactAppView.as_view()),
    path("hello/", HelloAPI),
    path("info/<str:id>", ItemAPI, name="get_info"),
    path("price/<str:id>", PriceAPI, name="get_price"),
    path("price/<str:id>/update", UpdateAPI.as_view(), name="update_item"),
    path("price/<str:id>/delete", DeleteAPI.as_view(), name="delete_item"),
]