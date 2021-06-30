from django.db import models
from django.conf import settings
from django.utils import timezone


class Item_Info(models.Model):
    pid =  models.CharField(max_length=200,null=False, primary_key=True)
    category_L = models.IntegerField()
    name = models.CharField(max_length=200)
    value = models.IntegerField()
    price = models.IntegerField()
         

    class Meta:
        managed = False
        db_table = 'item_info' # db 내부에 테이블 이름 설정