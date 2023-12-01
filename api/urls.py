from django.urls import path
from .views import *

urlpatterns = [
    path('notasventa/create/', NotasVentaCreateAPIView.as_view(), name='notasventa_create'),
    path('itemsnotaventa/create/', ItemsNotaVentaCreateAPIView.as_view(), name='itemsnotaventa_create'),
    path('<uuid:pk>/eliminarItem/', ItemsNotaVentaDeleteAPIView.as_view(), name='itemsnotaventa_delete'),
    # Otras URLs de la API aquí si es necesario
]