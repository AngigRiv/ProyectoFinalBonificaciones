from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from bonificacion.models import *
from .serializers import *
from django.shortcuts import get_object_or_404

class NotasVentaCreateAPIView(generics.CreateAPIView):
    queryset = NotasVenta.objects.all()
    serializer_class = NotasVentaSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Retorna la respuesta con el ID de la NotasVenta recién creada
        return Response({'notas_venta_id': serializer.data['nota_venta_id']}, status=status.HTTP_201_CREATED, headers=headers)
class ItemsNotaVentaCreateAPIView(generics.CreateAPIView):
    queryset = ItemsNotaVenta.objects.all()
    serializer_class = ItemsNotaVentaSerializer
    def create(self, request, *args, **kwargs):
        # Tu lógica de serialización y creación actual
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Verificar si se cumple el caso de bonificación
        bonificacion = False
        print(request.data.get('articulo_id'),request.data.get('cantidad', 0))
        print('request.data')
        if self.aplica_bonificacion(request.data):
            # Aplicar lógica de bonificación
            bonificacion = True
            self.aplicar_bonificacion(request.data)
        # Continuar con el proceso de creación
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Retorna la respuesta con el ID del ItemsNotaVenta recién creado y el indicador de bonificación
        return Response({'items_notaventa_id': serializer.data['item_id'], 'bonificacion': bonificacion}, status=status.HTTP_201_CREATED, headers=headers)
    
    def aplica_bonificacion(self, data):
        cantidad_comprada = data.get('cantidad', 0)
        articulo = get_object_or_404(Articulos, articulo_id=data.get('articulo_id'))
        return (int(cantidad_comprada) == 48 and str(articulo.codigo_sku )== '203101')
    
    def aplicar_bonificacion(self, data):
        articulo_bonificacion = get_object_or_404(Articulos, codigo_sku='200101B')
        cantidad_bonificacion = 2
        nota_venta = get_object_or_404(NotasVenta, nota_venta_id=data.get('nota_venta_id'))
        ItemsNotaVenta.objects.create(
            nota_venta_id=nota_venta,
            articulo_id=articulo_bonificacion,
            cantidad=cantidad_bonificacion,
            descuento_unitario=articulo_bonificacion.precio_unitario,
            es_bonificacion=True
        )
        
        
class ItemsNotaVentaDeleteAPIView(generics.DestroyAPIView):
    queryset = ItemsNotaVenta.objects.all()
    serializer_class = ItemsNotaVentaSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        # Actualizar el total_pedido después de la eliminación
        instance.nota_venta_id.update_total_pedido()
        return Response(status=status.HTTP_204_NO_CONTENT)