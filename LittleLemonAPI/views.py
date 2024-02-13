from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .serializers import (CategorySerializer, MenuItemSerializer,
                          ManagerSerializer,DeliveryCrewSerializer,
                          CartSerializer, OrderSerializer,
                          OrderItemSerializer
                          )
from .models import Category, MenuItem, Cart, Order, OrderItem
from .permissions import IsManager
from .paginations import CustomPagination
from .search_utils import custom_search, order_custom_search
from .filters import order_menu_items


class CategoryView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['title']
#     search_fields = ['title', 'category__title']

  
class MenuItemView(APIView):
    permission_classes =[IsAuthenticated, IsManager]
    ordering_fields = ['title']
    # pagination_class = CustomPagination
        
    def get(self, request, *args, **kwargs):
        search_param = request.query_params.get('search', None)
        ordering_param = request.query_params.get('ordering', 'id')
        
        menuitems = MenuItem.objects.all() 
        menuitems = custom_search(menuitems, search_param)
        menuitems = order_menu_items(menuitems, ordering_param) 
              
        paginator = CustomPagination()
        page = paginator.paginate_queryset(menuitems, request)
        
        serializer = MenuItemSerializer(page, many=True)
       
        return paginator.get_paginated_response(serializer.data)
    
   
    
    def post(self, request, *args, **kwargs):
        serialized_item = MenuItemSerializer(data=request.data)
        if serialized_item.is_valid():
            serialized_item.save()
            return Response(serialized_item.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
   
    def put(self, request, *args, **kwargs):
       return Response(status=status.HTTP_401_UNAUTHORIZED)
   
    def patch(self, request, *args, **kwargs):
       return Response(status=status.HTTP_401_UNAUTHORIZED)
   
    def delete(self, request, *args, **kwargs):
       return Response(status=status.HTTP_401_UNAUTHORIZED)
   

    
class MenuItemDetailView(APIView):
    permission_classes = [IsManager]
    
    def get_object(self, menu_id):
        return get_object_or_404(MenuItem, id=menu_id)
    
    
    def get(self, request, menu_id, *args, **kwargs):
        menu_item_obj = self.get_object(menu_id)
        serializer = MenuItemSerializer(menu_item_obj)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request, menu_id):
        menu_item_obj = self.get_object(menu_id)
        serializer = MenuItemSerializer(menu_item_obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, menu_id):
        menu_item_obj = self.get_object(menu_id)
        serializer = MenuItemSerializer(menu_item_obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,menu_item, *args, **kwargs):
        menu_item_obj = self.get_object(menu_item)
        menu_item_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
                
    
class Managers(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    def get(self, request, *args, **kwargs):
        manager_group = get_object_or_404(Group, name='Manager')
        if manager_group in request.user.groups.all():
            manager_users = User.objects.filter(groups=manager_group)
            serializer = ManagerSerializer(manager_users, many=True)
            return Response(serializer.data)
        return Response({'error': 'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = User.objects.get(username=username)
            manager_group = Group.objects.get(name='DeliveryCrew')
            manager_group.user_set.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class DeleteMangerUserView(APIView):
    def delete(self, request, user_id, *args, **kwargs):
            user = get_object_or_404(User, id=user_id)
            manager_group = get_object_or_404(Group, name='Manager')
            if user.groups.filter(name=manager_group):
                manager_group.user_set.remove(user)
                return Response(status=status.HTTP_200_OK)
            return Response({'error': 'User don\'t have this group'}, status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewView(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    
    def get(self, request, *args, **kwargs):
        delivery_group = get_object_or_404(Group, name='DeliveryCrew')
        manager_group = get_object_or_404(Group, name='Manager')
        
        if manager_group in request.user.groups.all():
            delivery_crew_user = User.objects.filter(groups=delivery_group)
            serializer = DeliveryCrewSerializer(delivery_crew_user, many=True)
            return Response(serializer.data)
        return Response({'error': 'Permission denied'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        serializer = DeliveryCrewSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            delivery_crew = get_object_or_404(Group, name='DeliveryCrew')
            delivery_crew.user_set.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteDeliveryCrew(APIView):
    def delete(self, request,user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        delivery_crew = get_object_or_404(Group, name='DeliveryCrew')
        if  user.groups.filter(name=delivery_crew):
            delivery_crew.user_set.remove(user)      
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'User don\'t belong to this group'}, status=status.HTTP_404_NOT_FOUND)
        

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cart_item = Cart.objects.all()
        serializer = CartSerializer(cart_item, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id 
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        # delete the menuitem attach to the current user  
        user_cart = Cart.objects.filter(user=request.user)
        user_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get(self, request, *args, **kwargs):
        manager_group = get_object_or_404(Group, name='Manager')
        delivery_group = get_object_or_404(Group, name='DeliveryCrew')
        search_param = request.query_params.get('search', None)        
                
        if request.user.groups.filter(name=manager_group):
            # search_param = request.query_params.get('search', None)
            orders = Order.objects.all().order_by('id')
            orders = order_custom_search(orders, search_param)
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(orders, request)
            serializer = OrderSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)  
            
        elif request.user.groups.filter(name=delivery_group):       
            delivery_crew_order = Order.objects.filter(delivery_crew=request.user)
            delivery_crew_order = order_custom_search(delivery_crew_order, search_param)
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(delivery_crew_order, request)
            serializer = OrderSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        else:      
            get_current_user = self.request.user
            print(get_current_user)
            user_orders = Order.objects.filter(user=get_current_user)
            user_orders = order_custom_search(user_orders, search_param)
                
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(user_orders, request)
            serializer = OrderSerializer(result_page, many=True)  
            return paginator.get_paginated_response(serializer.data)
        
    # def post(self, request, *args, **kwargs):
        
    #     date = request.data.get('date')
    #     order = Order.objects.create(user=self.request.user, date=date, total=0)
    #     serializer = OrderSerializer(order)
    #     # serializer.is_valid(raise_exception=True)
    #     # serializer.save()
    #     return Response(serializer.data)
    
    
    def post(self, request, *args, **kwargs):
        
        # Get the current user cart item
        cart_items = Cart.objects.filter(user=request.user)
        
        date = request.data.get('date')
    
        # Create a new order
        order = Order.objects.create(user=request.user, total=0, date=date)
        
        # order = Order.objects.filter(user=request.user)
        
        # Create a new order item for each cart item
        total_price = 0
        for item in cart_items:
            order_item_data = {
            'order': order.id,
            'menuitem': item.menuitem.id,
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'price': item.price
            }
            
            order_item_serializer = OrderItemSerializer(data=order_item_data)
            if order_item_serializer.is_valid():
                order_item_serializer.save()
                total_price += item.price
                
        order.total = total_price
        order.save()
        
        cart_items.delete()
        
        order_items = OrderItem.objects.filter(order=order)
        created_order = OrderItemSerializer(order_items, many=True).data
        
        return Response(created_order, status=status.HTTP_201_CREATED)


class OrderDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, order_id):
        return get_object_or_404(Order, id=order_id)
    
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            orderItem_queryset = OrderItem.objects.filter(order=order)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or does not belong to the current user.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemSerializer(orderItem_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, order_id, *args, **kwargs):
        order = self.get_object(order_id)  
        manager_group = get_object_or_404(Group, name='Manager')
        delivery_crew_group = get_object_or_404(Group, name='DeliveryCrew')
                
        if request.user.groups.filter(name=manager_group):
            serilalizer = OrderSerializer(order, data=request.data, partial=True)
            serilalizer.is_valid(raise_exception=True)
            serilalizer.save()
            return Response(serilalizer.data, status=status.HTTP_200_OK)
        
        elif request.user.groups.filter(name=delivery_crew_group):
            if 'status' in request.data and len(request.data) == 1:
                serilalizer = OrderSerializer(order, data=request.data, partial=True)
                serilalizer.is_valid(raise_exception=True)
                serilalizer.save()
                return Response(serilalizer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Delivery crew is only allowed to update the order status.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request, order_id, *args, **kwargs):
        order = self.get_object(order_id)
        manager_group = get_object_or_404(Group, name='Manager')
        
        if request.user.groups.filter(name=manager_group):
            serializer = OrderSerializer(order, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, order_id,  *args, **kwargs):
        manager_group = get_object_or_404(Group, name='Manager')
        if request.user.groups.filter(name=manager_group):
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'permission denied.'})
    
