from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework import serializers
from django.contrib.auth.models import Group, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug', 'title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())   
    class Meta:
        model = MenuItem
        fields = ['id','title', 'price', 'featured', 'category']       
     
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email'] 
        
class CartSerializer(serializers.ModelSerializer):
    menuitem_name = serializers.ReadOnlyField(source='menuitem.title')
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2) 

    class Meta:
        model = Cart
        fields = ['id','menuitem_name','menuitem', 'quantity', 'price'] 
        read_only_fields = ['user']  

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem_title = serializers.ReadOnlyField(source='menuitem.title')
    class Meta:
        model = OrderItem
        fields = ['menuitem','menuitem_title','quantity', 'unit_price', 'price']

            
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='orderitem_set')
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'items']
        read_only_fields = ['id', 'user', 'total', 'date'] 

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # Manager: only assign the delivery-crew and change status
        if user.groups.filter(name='manager').exists():
            instance.delivery_crew = validated_data.get('delivery_crew', instance.delivery_crew)
            instance.status = validated_data.get('status', instance.status)
        
        # Delivery crew pode apenas alterar o status
        elif user.groups.filter(name='delivery-crew').exists():
            if 'status' in validated_data:
                instance.status = validated_data['status']
            else:
                raise serializers.ValidationError("The delivery crew must provide a status.")
        
        elif user.groups.filter(name='customer').exists():
            raise serializers.ValidationError("Customers cannot change the status or the delivery team.")

        instance.save()
        return instance        
    
