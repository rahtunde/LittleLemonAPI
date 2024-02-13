from rest_framework import permissions, status
from django.contrib.auth.models import User, Group


class MenuItemsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        else:
            return False
        
        
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        managers = Group.objects.get(name='Manager')
        # Check if user is in the "manager" group for global permissions (POST)
        return request.user.groups.filter(name=managers).exists()
    
    
# class IsDeliveryCrew(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ['GET']:
#             return True
#         delivery_crew = Group.objects.get(name='DeliveryCrew')
#         return request.user.groups.filter(name=delivery_crew).exists()