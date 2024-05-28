from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Для ModelSerializer импортируем нашы модели:
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:  # Внутренний класс в котором будет указаны какая модель используется и её поля
        model = Product
        fields = ['id','title','description']
        
    def validate(self, attrs):  # Проверка на запрещённый текст любых атрибутах при создании пользователем
        if 'какашка' in attrs['title']:
            raise ValidationError('Вы использовали запретное слово')
        return attrs
    
    def create(self, validated_data):  # вот так сериализатор создаёт данные
        print(validated_data)
        return super().create(validated_data)
    
     
    


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:  # Внутренний класс в котором будет указаны какая модель используется и её поля
        model = StockProduct
        fields = ['id','stock','product','quantity','price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    
    # настройте сериализатор для склада
    class Meta:  # Внутренний класс в котором будет указаны какая модель используется и её поля
        model = Stock
        fields = ['id','address','positions']
        
    def validate(self, attrs):  # Проверка на запрещённый текст любых атрибутах при создании пользователем
        if 'какашка' in attrs['address']:
            raise ValidationError('Вы использовали запретное слово')
        return attrs



    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        
        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, defaults=position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        product = super().create(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, product=product, defaults=position)

        return stock
