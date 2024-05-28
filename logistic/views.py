from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination

# Наши модельки и сериализаторы:
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from django_filters import rest_framework as filters


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # при необходимости добавьте параметры фильтрации
    # Добавляем фильтры
    filter_backends = [DjangoFilterBackend, SearchFilter]  # включим все доступные фильтры
    filter_fields = ['title','description']  # фильтрация по полям
    #search_fields = ['text',]  # сканируем поле ['text',].
    #ordering_fields = ['id','user','text','created_at']  # Список параметров по которым можно будет упорядочевать
    
    # Добавляем пагинатор
    pagination_class = LimitOffsetPagination  # В строке запроса нужно будет указывать два параметра limit - сколько показать объектов и offset - сколько пропустить
    


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    
    # при необходимости добавьте параметры фильтрации
    # Добавляем фильтры
    filter_backends = [DjangoFilterBackend, SearchFilter]  # включим все доступные фильтры
    filter_fields = ['address','products']  # фильтрация по полям
    
    # Добавляем пагинатор
    pagination_class = LimitOffsetPagination  # В строке запроса нужно будет указывать два параметра limit - сколько показать объектов и offset - сколько пропустить
    
# Equivalent FilterSet:
class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ('title',)