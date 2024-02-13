import django_filters
from .models import MenuItem, Order
from django.db.models import Q
from rest_framework.filters import OrderingFilter


def order_menu_items(queryset, ordering_param):
    return queryset.order_by(ordering_param)

