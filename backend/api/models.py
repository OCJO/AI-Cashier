from django.db import models
from django.conf import settings
from django.utils import timezone

'''
DB
----- 
1. 상품 정보 테이블
    - pid / category_L / name / price
2. 재고 테이블
    - pid / value / modify_date
'''
class Item_Info(models.Model):
    pid =  models.CharField(max_length=200,null=False, primary_key=True)
    category_L = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return self.title 

class Item_Stock(models.Model):
    pid =  models.CharField(max_length=200,null=False, primary_key=True)
    value = models.IntegerField()
    modify_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title