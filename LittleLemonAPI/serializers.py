from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Category, Order, OrderItem, MenuItem, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title', 'price', 'featured', 'category']
        

class ManagerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
      
  
class DeliveryCrewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)  
    

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','user', 'menuitem', 'quantity', 'unit_price', 'price'] 

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
        
        
class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew','status', 'total', 'date', 'order_item']

# class PostOrderSerializer(serializers.Serializer):
#     date = serializers.DateField()