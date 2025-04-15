from django_filters import rest_framework as filters
from .models import MenuItem, Category

class MenuItemFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug', lookup_expr='iexact')  
    price = filters.NumberFilter(field_name='price', lookup_expr='exact')
    
    class Meta:
        model = MenuItem
        fields = [ 'category','price', ]