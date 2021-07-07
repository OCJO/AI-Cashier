
from rest_framework import serializers
from .models import Item_Info,Item_Stock


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Info
        fields = ('pid', 'name', 'price')

 

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Stock
        fields = ('pid','value','modify_date')