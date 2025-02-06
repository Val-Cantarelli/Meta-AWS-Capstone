from rest_framework import viewsets
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, CartSerializer, OrderSerializer
from rest_framework.permissions import IsAdminUser, BasePermission, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from .filters import MenuItemFilter
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.filters import OrderingFilter

from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)

class IsDeliveryCrew(BasePermission):
        def has_permission(self, request, view):
            return request.user.groups.filter(name='delivery-crew').exists()
     
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()

class IsCustomer(BasePermission):
     def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return not request.user.groups.filter(name__in=['delivery-crew', 'manager']).exists()

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.groups.filter(name='manager').exists()
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()] 

class MenuItemsViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer 
    
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)  
    filterset_class = MenuItemFilter
    ordering_fields=['price']
    search_fields = ['title','category__slug','id'] 

    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        else:
            return [IsAdminOrManager()]
    
class ManagerViewSet(viewsets.ViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated,IsAdminOrManager]
           
    def get_queryset(self):
        group_name = self.kwargs.get('group_name')  
        return User.objects.filter(groups__name=group_name)
    
    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        username = request.data.get('username') 
        group_name = self.kwargs.get('group_name')

        if not username: return Response({"error": "'username' field is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username) 
            group = Group.objects.get(name=group_name)

            if user.groups.filter(name=group_name).exists():
                return Response({"message": f"User '{username}' is already in group '{group_name}'."},
                                status=status.HTTP_400_BAD_REQUEST)

            user.groups.add(group) 
            return Response({"message": f"User '{username}' added to group '{group_name}'."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')  
        group_name = self.kwargs.get('group_name')

        try:
            user = User.objects.get(id=user_id)  
            group = Group.objects.get(name=group_name)

            if not user.groups.filter(name=group_name).exists():
                return Response({"message": f"User '{user.username}' is not in the '{group_name}' group."}, 
                                status=status.HTTP_404_NOT_FOUND)

            user.groups.remove(group)
            return Response({"message": f"User '{user.username}' removed from group '{group_name}'."}, 
                            status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

class CartViewSet(viewsets.ViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def list(self, request):
        items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        menu_item_id = request.data.get('menuitem')
        quantity = request.data.get('quantity')

        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)

        unit_price = menu_item.price
        total_price = unit_price * int(quantity)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menu_item,
            defaults={
                'quantity': quantity,
                'unit_price': unit_price,
                'price': total_price
            }
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.price = cart_item.quantity * unit_price
            cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        deleted_count, _ = Cart.objects.filter(user=request.user).delete()
        if deleted_count > 0:
            return Response({"message": "Item(s) deleted."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No items to delete."}, status=status.HTTP_200_OK)
    
class OrdersViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='manager').exists():
            return Order.objects.all()
        
        elif user.groups.filter(name='delivery-crew').exists():
            return Order.objects.filter(delivery_crew=user)

        return Order.objects.filter(user=user)
       
    def retrieve(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['pk'])
            if request.user != order.user and not request.user.groups.filter(name='manager').exists() and request.user != order.delivery_crew:
                raise PermissionDenied("You do not have permission to acess this information.")

            serializer = self.get_serializer(order)
            
            return Response(serializer.data)
        
        
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)  
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
           
    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        delivery_user_id = request.data.get('delivery_crew')

       
        if delivery_user_id:
            try:
                user = User.objects.get(id=delivery_user_id)
                delivery_crew_group = Group.objects.get(name='delivery-crew')
                
                if user not in delivery_crew_group.user_set.all():
                    
                    raise ValidationError("The assigned user is not part of the 'delivery-crew' group.")
            except User.DoesNotExist:
                raise ValidationError("User not found.")
        
        serializer = self.get_serializer(order, data=request.data, partial=True)  
        serializer.is_valid(raise_exception=True)  
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_200_OK)  
        
    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return Response({"detail": "The cart is empty!"}, status=400)

        order = Order.objects.create(user=request.user, total=sum(item.price for item in cart_items))
        order_items = []
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
            order=order,
            menuitem=cart_item.menuitem,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            price=cart_item.price
        )
        order_items.append({
            "menuitem": order_item.menuitem.title,
            "quantity": order_item.quantity,
            "unit_price": str(order_item.unit_price),  
            "price": str(order_item.price) 
        })

        cart_items.delete()

        return Response({
        "order_id": order.id,
        "total": str(order.total),
        "items": order_items,
        "detail": "Order created!"
    }, status=201)
    
    