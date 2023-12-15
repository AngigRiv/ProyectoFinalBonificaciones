from pyexpat.errors import messages
from urllib import request
from wsgiref import headers
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from bonificacion.forms import NotasVentaForm
from django.db.models import Q
from bonificacion.models import *
from bonificacion.views import NotasVentaCreateView, NotasVentaDeleteView, NotasVentaListView
from .serializers import *
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from datetime import datetime

class NotasVentaCreateAPIView(generics.CreateAPIView):
    queryset = NotasVenta.objects.all()
    serializer_class = NotasVentaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'notas_venta_id': serializer.data['nota_venta_id']}, status=status.HTTP_201_CREATED, headers=headers)

class ItemsNotaVentaCreateAPIView(generics.CreateAPIView):
    queryset = ItemsNotaVenta.objects.all()
    serializer_class = ItemsNotaVentaSerializer

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bonificacion = False

        if self.aplica_bonificacion(request.data):
            bonificacion = True
            nota_venta = get_object_or_404(NotasVenta, nota_venta_id=request.data.get('nota_venta_id'))
            self.aplicar_bonificacion_formula(request.data, nota_venta)

        nota_venta = get_object_or_404(NotasVenta, nota_venta_id=request.data.get('nota_venta_id'))

        # Verifica si el artículo ya existe en NotaVenta
        articulo = get_object_or_404(Articulos, articulo_id=request.data.get('articulo_id'))
        existing_item = ItemsNotaVenta.objects.filter(
            nota_venta_id=nota_venta,
            articulo_id=articulo,
            es_bonificacion=False
        ).first()

        if existing_item:
            # Actualiza la cantidad para el artículo existente
            existing_item.cantidad += int(request.data.get('cantidad', 0))
            existing_item.save()

            headers = self.get_success_headers(serializer.data)

            # Obtener los elementos actualizados después de agregar uno nuevo
            updated_items = ItemsNotaVenta.objects.filter(nota_venta_id=nota_venta)

            # Renderizar el HTML actualizado
            html = render_to_string('templates/itemsnotaventa_list.html', {'object_list': updated_items}, request=request)

            # Devolver JSON con el HTML actualizado y un indicador de éxito
            return JsonResponse({'success': True, 'html': html}, status=status.HTTP_201_CREATED, headers=headers)

        last_nro_item = ItemsNotaVenta.objects.filter(nota_venta_id=nota_venta).aggregate(Max('nro_item'))['nro_item__max']
        nro_item = 1 if last_nro_item is None else last_nro_item + 1

        serializer.save(nro_item=nro_item)

        headers = self.get_success_headers(serializer.data)

        # Obtener los elementos actualizados después de agregar uno nuevo
        updated_items = ItemsNotaVenta.objects.filter(nota_venta_id=NotasVentaCreateView)

        # Renderizar el HTML actualizado
        html = render_to_string('templates/itemsnotaventa_list.html', {'object_list': updated_items}, request=request)

        # Obtener el nuevo subtotal y total
        subtotal_venta = NotasVentaDeleteView.itemsnotaventa_set.aggregate(Sum('total_item_bruto'))['total_item_bruto__sum'] or 0
        total_venta = NotasVentaListView.itemsnotaventa_set.aggregate(Sum('total_item'))['total_item__sum'] or 0

        # Devolver JSON con el HTML actualizado, subtotal y total
        return JsonResponse({'success': True, 'html': html, 'subtotal': subtotal_venta, 'total': total_venta}, status=status.HTTP_201_CREATED, headers=headers)

    def aplica_bonificacion(self, data):
        cantidad_comprada = int(data.get('cantidad', 0))
        articulo = get_object_or_404(Articulos, articulo_id=data.get('articulo_id'))
        fecha_venta = datetime.now()
        promociones_activas = Promociones.objects.filter(
            fecha_inicio__lte=fecha_venta,
            fecha_fin__gte=fecha_venta
        )

        # Obtener el cliente de la nota de venta
        nota_venta = get_object_or_404(NotasVenta, nota_venta_id=data.get('nota_venta_id'))
        cliente = nota_venta.cliente_id

        for promocion in promociones_activas:
            if FormulaDetalle.objects.filter(
                promocion_id=promocion,
                articulos_seleccionar=articulo,
                cantidad_a_comprar=cantidad_comprada,
                canal_cliente=cliente.canal_cliente_id
            ).exists():
                return True

        return False

    def aplicar_bonificacion_formula(self, data, nota_venta):
        articulo_id = data.get('articulo_id')
        cantidad_comprada = int(data.get('cantidad', 0))

        # Obtener el cliente de la nota de venta
        cliente = nota_venta.cliente_id

        formulas_activas = FormulaDetalle.objects.filter(
            promocion_id__fecha_inicio__lte=datetime.now(),
            promocion_id__fecha_fin__gte=datetime.now(),
            articulos_seleccionar=articulo_id,
            cantidad_a_comprar=cantidad_comprada,
            canal_cliente=cliente.canal_cliente_id
        )

        for formula in formulas_activas:
            articulo_a_bonificar = formula.articulo_a_bonificar
            cantidad_a_bonificar = formula.cantidad_a_bonificar

            # Buscar la bonificación existente para el artículo de la fórmula
            bonificacion_existente = ItemsNotaVenta.objects.filter(
                nota_venta_id=nota_venta,
                articulo_id=articulo_a_bonificar,
                es_bonificacion=True
            ).first()

            if bonificacion_existente:
                # Actualizar la cantidad para la bonificación existente
                bonificacion_existente.cantidad += cantidad_a_bonificar
                bonificacion_existente.save()
            else:
                # Crear la bonificación si no existe
                bonificacion = ItemsNotaVenta.objects.create(
                    nota_venta_id=nota_venta,
                    articulo_id=articulo_a_bonificar,
                    cantidad=cantidad_a_bonificar,
                    descuento_unitario=cantidad_a_bonificar * articulo_a_bonificar.precio_unitario,
                    total_item_bruto=cantidad_a_bonificar * articulo_a_bonificar.precio_unitario,
                    factor_descuento=1,
                    total_item=0,
                    es_bonificacion=True
                )

                # Actualizar el número de item de la bonificación
                last_nro_item_bonificacion = ItemsNotaVenta.objects.filter(
                    nota_venta_id=nota_venta,
                    es_bonificacion=True
                ).aggregate(Max('nro_item'))['nro_item__max']
                bonificacion.nro_item = 1 if last_nro_item_bonificacion is None else last_nro_item_bonificacion + 1
                bonificacion.save()

            # Mensaje de depuración
            print(f"Aplicando bonificación para artículo: {articulo_a_bonificar.descripcion}")

class ItemsNotaVentaDeleteAPIView(generics.DestroyAPIView):
    queryset = ItemsNotaVenta.objects.all()
    serializer_class = ItemsNotaVentaSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Obtener la nota de venta y el número de ítem
        nota_venta = instance.nota_venta_id
        nro_item = instance.nro_item

        # Dentro de una transacción para garantizar la atomicidad de la operación
        with transaction.atomic():
            # Obtener todas las bonificaciones y el ítem principal para eliminarlos
            items_a_eliminar = ItemsNotaVenta.objects.filter(
                Q(nota_venta_id=nota_venta, nro_item=nro_item) |
                Q(nota_venta_id=nota_venta, es_bonificacion=True, nro_item__lt=nro_item)
            )

            # Eliminar los ítems y bonificaciones
            items_a_eliminar.delete()

            # Actualizar el total_pedido después de la eliminación
            nota_venta.update_total_pedido()

        return Response(status=status.HTTP_204_NO_CONTENT)