from rest_framework.urls import path
from .views import MenuItemsViewSet, CategoryViewSet, ManagerViewSet, CartViewSet,OrdersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'menu-items', MenuItemsViewSet)
router.register(r'categories', CategoryViewSet)

# Custom URLs with proper type hints for better OpenAPI documentation
from django.urls import path, include

custom_patterns = [
    # Group management with integer user IDs (no trailing slash)
    path('groups/<str:group_name>/users', ManagerViewSet.as_view({'get': 'list', 'post': 'create'}), name='group-users-list'),
    path('groups/<str:group_name>/users/<int:pk>', ManagerViewSet.as_view({'delete': 'destroy'}), name='group-users-detail'),
    
    # Orders with integer IDs (no trailing slash)
    path('orders', OrdersViewSet.as_view({'get': 'list', 'post': 'create'}), name='orders-list'),
    path('orders/<int:pk>', OrdersViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='orders-detail'),
    
    # Cart with integer IDs (no trailing slash)
    path('cart', CartViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart-list'),
    path('cart/<int:pk>', CartViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'}), name='cart-detail'),
]

urlpatterns = list(router.urls) + custom_patterns