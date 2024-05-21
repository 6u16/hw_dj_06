from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=60, unique=True)
    description = models.TextField(null=True, blank=True)


class Stock(models.Model):
    address = models.CharField(max_length=200, unique=True)
    products = models.ManyToManyField(Product, through='StockProduct', related_name='stocks')


class StockProduct(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='positions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='positions')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=18, decimal_places=2) #, validators=[MinValueValidator(0)])
    


# Сделаем миграции и загрузим модель в БД:
'''python manage.py makemigrations'''# - произойдёт создание 0001_initial.py в папке migrations, где будут указаны миграции

# А теперь эти миграции нужно применить, чтобы создать необходимую структуру БД, если БД отсутствует то будет создана и она
'''python manage.py migrate'''# - применение миграции
