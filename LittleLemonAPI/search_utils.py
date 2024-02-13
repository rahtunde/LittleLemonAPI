from django.db.models import Q


def custom_search(queryset, search_param):
    if search_param:
        query = Q(title__icontains=search_param) | Q(category__title__icontains=search_param)
        return queryset.filter(query)
    return queryset


def order_custom_search(queryset, search_param):
    if search_param:
        query = Q(date__icontains=search_param) | Q(delivery_crew__username__icontains=search_param)
        return queryset.filter(query)
    return queryset