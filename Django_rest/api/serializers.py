
from rest_framework import serializers
from .models import Item_Info


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Info
        fields = ('pid', 'category_L', 'name', 'value','price')

 
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Info
        fields = ('pid','price')

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Info
        fields = ('pid','value')