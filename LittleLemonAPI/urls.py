from django.urls import path
from . import views


urlpatterns = [
    path('menu-items/', views.MenuItemView.as_view(), name='menu-item'),
    path('menu-items/<int:menu_id>', views.MenuItemDetailView.as_view(), name='menu-item'),
    path('categories', views.CategoryView.as_view(), name='category'),
    path('groups/manager/users', views.Managers.as_view(), name='managers'),
    path('groups/manager/users/<int:user_id>', views.DeleteMangerUserView.as_view(), name='delete-manager'),
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view(), name='delivery-crew'),
    path('groups/delivery-crew/users/<int:user_id>', views.DeleteDeliveryCrew.as_view(), name='delete-delivery-crew'),
    path('cart/menu-items', views.CartView.as_view(), name='cart-menu-item'),
    path('cart/orders', views.OrderView.as_view(), name='orders'),
    path('orders/<int:order_id>', views.OrderDetailsView.as_view(), name='orders-details'),
    
    
]