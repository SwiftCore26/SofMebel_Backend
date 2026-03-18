from django_filters import FilterSet, CharFilter, NumberFilter

from apps.models import Product


class ProductFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')
    product_name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'product_name']
