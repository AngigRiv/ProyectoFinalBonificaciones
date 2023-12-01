from rest_framework import serializers
from bonificacion.models import *

class NotasVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotasVenta
        fields = '__all__'

class ItemsNotaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsNotaVenta
        fields = '__all__'
