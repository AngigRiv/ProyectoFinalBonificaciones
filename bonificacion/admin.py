from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Empresa)
admin.site.register(Sucursales)
admin.site.register(Articulos)
admin.site.register(GruposProveedor)
admin.site.register(LineasArticulos)
admin.site.register(SublineasArticulos)
admin.site.register(Marcas)
admin.site.register(Usuario)
admin.site.register(CanalCliente)
admin.site.register(Clientes)
admin.site.register(TiposIdentificacion)
admin.site.register(TiposPedido)
admin.site.register(Vendedores)
admin.site.register(NotasVenta)
admin.site.register(CondicionesVenta)
admin.site.register(ItemsNotaVenta)