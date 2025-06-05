from rest_framework.urls import path
from .views import MenuItemsViewSet, CategoryViewSet, ManagerViewSet, CartViewSet,OrdersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'menu-items', MenuItemsViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'groups/(?P<group_name>manager|delivery-crew)/users', ManagerViewSet, basename='group-users')
router.register(r'orders', OrdersViewSet, basename='orders'),
router.register(r'cart', CartViewSet, basename='cart'),

urlpatterns = [
    # This route allows the 'deletion' of a user from a specific group by passing the group name and user ID in the URL.DefaultRouter() doesnt 
    path('groups/<str:group_name>/users/<int:user_id>/', ManagerViewSet.as_view({'delete': 'destroy'}), name='group-user-detail'),
    
    
    # This route allows the 'deletion' of a user from a specific group by passing the group name and user ID in the URL.
    #(redundant)path('cart', CartViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='cart'),
    # This route allows the 'deletion' of a user from a specific group by passing the group name and user ID in the URL.
    #(redundant)path('cart/orders/', OrdersViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='cart-orders'),
]

urlpatterns += router.urls