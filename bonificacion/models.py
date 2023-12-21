from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from bonificacion.manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from django.db import models, transaction
from django.utils import timezone
from django.db.models.signals import pre_save

from django.dispatch import receiver
from django.db.models import Sum

class Usuario(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    fullname = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=150, null=True)
    
    # Agregar related_name para evitar conflictos
    groups = models.ManyToManyField('auth.Group', related_name='usuario_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuario_user_permissions', blank=True)

    objects = CustomUserManager()
      
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fullname']
        
    def _str_(self):
        return self.email

class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nro_documento = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.razon_social}"

class Sucursales(models.Model):
    sucursal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre_comercial = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.nombre_comercial}"

class GruposProveedor(models.Model):
    grupo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    codigo_grupo = models.CharField(max_length=15)
    grupo_descripcion = models.CharField(max_length=100)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    activo = models.BooleanField()
    responsable_grupo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='grupos_proveedor')
    def __str__(self):
        return f"{self.grupo_descripcion}"

class LineasArticulos(models.Model):
    linea_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    codigo_linea = models.CharField(max_length=15)
    linea_descripcion = models.CharField(max_length=100)
    grupo_id = models.ForeignKey(GruposProveedor, on_delete=models.CASCADE)
    activo = models.BooleanField()
    responsable_linea = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.linea_descripcion}"

class SublineasArticulos(models.Model):
    sublinea_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    codigo_sublinea = models.CharField(max_length=15)
    sublinea_descripcion = models.CharField(max_length=100)
    linea_id = models.ForeignKey(LineasArticulos, on_delete=models.CASCADE)
    estado = models.BooleanField()
    def __str__(self):
        return f"{self.sublinea_descripcion}"

class UnidadesMedida(models.Model):
    unidad_medida_id = models.CharField(primary_key=True, max_length=10)
    unidad_nombre = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.unidad_nombre}"

class Marcas(models.Model):
    marca_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    codigo_marca = models.CharField(max_length=14)
    marca_nombre = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.marca_nombre}"

class Articulos(models.Model):
    articulo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    codigo_sku = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=150)
    unidad_medida_id = models.ForeignKey(UnidadesMedida, on_delete=models.CASCADE)
    grupo_id = models.ForeignKey(GruposProveedor, on_delete=models.CASCADE)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    linea_id = models.ForeignKey(LineasArticulos, on_delete=models.CASCADE)
    sublinea_id = models.ForeignKey(SublineasArticulos, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    factor_compra = models.IntegerField()
    factor_reparto = models.IntegerField()
    marca_id = models.ForeignKey(Marcas, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descripcion} - S/. {self.precio_unitario}"

class CanalCliente(models.Model):
    canal_cliente_id = models.CharField(primary_key=True, max_length=2)
    ESTADOS = (
        ('Mayoristas', 'Mayoristas'),
        ('Cobertura', 'Cobertura'),
        ('Mercado', 'Mercado'),
        ('Institucionales', 'Institucionales'),
    )
    canal_cliente_descripcion  = models.CharField(max_length=150, choices=ESTADOS, default='M')
    def __str__(self):
        return f"{self.canal_cliente_descripcion}"  

class TiposIdentificacion(models.Model):
    tipo_identificacion_id = models.CharField(primary_key=True, max_length=2)
    tipo_identificacion_nombre = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.tipo_identificacion_nombre}"     
class Clientes(models.Model):
    cliente_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    tipo_identificacionC_id = models.ForeignKey(TiposIdentificacion, on_delete=models.CASCADE)
    nro_documento = models.CharField(max_length=12)
    nombre_razon_social = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    canal_cliente_id = models.ForeignKey(CanalCliente, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre_razon_social} - {self.nro_documento}"  
     
class TiposPedido(models.Model):
    tipo_pedido_id = models.CharField(primary_key=True, max_length=3)
    tipo_pedido_nombre = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.tipo_pedido_nombre} "  
     
class Vendedores(models.Model):
    vendedor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    vendedor_codigo = models.CharField(max_length=15)
    tipo_identificacion_id = models.ForeignKey(TiposIdentificacion, on_delete=models.CASCADE)
    nro_documento = models.CharField(max_length=11)
    nombres = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    correo_electronico = models.EmailField(max_length=255)
    nro_movil = models.CharField(max_length=15)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombres} - {self.nro_documento} "  
    
class CondicionesVenta(models.Model):
    condicion_venta = models.CharField(primary_key=True, max_length=3)
    SELECCIONES_CHOICES = (
        ('Con rango', 'Con Rango'),
        ('Minimo', 'Minimo'),
        ('Minimo hasta sin fin', 'Minimo hasta sin fin'),
    )
    descripcion  = models.CharField(max_length=150, choices=SELECCIONES_CHOICES, default='M')
    def __str__(self):
        return f"{self.descripcion}"
    
class NotasVenta(models.Model):
    nota_venta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    sucursal_id = models.ForeignKey(Sucursales, on_delete=models.CASCADE)
    nro_pedido = models.CharField(max_length=25, null=True)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    tipo_pedido_id = models.ForeignKey(TiposPedido, on_delete=models.CASCADE)
    cliente_id = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    condicion_venta = models.ForeignKey(CondicionesVenta, on_delete=models.CASCADE)
    plazo = models.IntegerField()
    tipo_documento = models.CharField(max_length=2)
    total_pedido = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    def update_total_pedido(self):
        with transaction.atomic():
            # Calcula el subtotal sumando los valores de total_item_bruto en ItemsNotaVenta
            subtotal_pedido = self.itemsnotaventa_set.aggregate(Sum('total_item_bruto'))['total_item_bruto__sum'] or 0

            # Calcula el total sumando los valores de total_item en ItemsNotaVenta
            total_pedido = self.itemsnotaventa_set.aggregate(Sum('total_item'))['total_item__sum'] or 0

            self.total_pedido = total_pedido
            print(f'Total Pedido actualizado en update_total_pedido: {self.total_pedido}')
            self.save()

@receiver(pre_save, sender=NotasVenta)
def set_numero_pedido(sender, instance, **kwargs):
    if instance._state.adding and not instance.nro_pedido:
        ultimo_numero = NotasVenta.objects.filter(cliente_id_id=instance.cliente_id).aggregate(models.Max('nro_pedido'))['nro_pedido__max']
        
        if ultimo_numero and ultimo_numero.isdigit():
            nuevo_numero = int(ultimo_numero) + 1
        else:
            nuevo_numero = 1
        instance.nro_pedido = f'n{nuevo_numero}'
        
class ItemsNotaVenta(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nota_venta_id = models.ForeignKey('NotasVenta', on_delete=models.CASCADE)
    nro_item = models.IntegerField(null=True)
    articulo_id = models.ForeignKey('Articulos', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    total_item_bruto = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    factor_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_item = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    es_bonificacion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.articulo_id.descripcion} - subtotal: {self.total_item_bruto}"

    def save(self, *args, **kwargs):
        if not self.total_item_bruto:
            self.total_item_bruto = self.cantidad * self.articulo_id.precio_unitario
        last_nro_item = ItemsNotaVenta.objects.filter(nota_venta_id=self.nota_venta_id).aggregate(Max('nro_item'))['nro_item__max']
        self.nro_item = 1 if last_nro_item is None else last_nro_item + 1
        self.descuento_unitario = self.total_item_bruto * self.factor_descuento
        self.total_item_bruto = self.cantidad * self.articulo_id.precio_unitario
        self.total_item = self.total_item_bruto - self.descuento_unitario
        super().save(*args, **kwargs)

        # Llama al método para actualizar total_pedido después de guardar un nuevo item
        self.nota_venta_id.update_total_pedido()

class Promociones(models.Model):
    promocion_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.descripcion} "  
            
class FormulaDetalle(models.Model):
    formula_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    descripcion = models.CharField(max_length=100)
    promocion_id = models.ForeignKey(Promociones, on_delete=models.CASCADE)
    productos_a_comprar = models.IntegerField(default=3)  # Establece el valor predeterminado en 3
    articulo_a_bonificar = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    articulos_seleccionar = models.ManyToManyField(Articulos, related_name='formuladetalle_seleccionar')
    cantidad_a_comprar = models.IntegerField(default=1)
    cantidad_a_bonificar = models.IntegerField(default=1)
    canal_cliente = models.ForeignKey(CanalCliente, on_delete=models.CASCADE, default=None, null=True, blank=True)
    def __str__(self):
        return f"{self.descripcion}"

class Descuentos(models.Model):
    descuento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cantidad_total_minima_venta = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_total_maxima_venta = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sin_limite_venta = models.BooleanField(default=False, null=True, blank=True)
    rango_venta = models.BooleanField(default=False, null = True)
    porcentaje_descuento = models.IntegerField()
    linea_producto = models.ForeignKey(LineasArticulos, on_delete=models.CASCADE)
    cantidad_minimo_productos = models.IntegerField(null=True, blank=True)
    cantidad_maxima_productos = models.IntegerField(null=True, blank=True)
    sin_limite_productos = models.BooleanField(default=False, null=True, blank=True)
    rango_productos = models.BooleanField(default=False, null = True)
    limitar_clientes = models.BooleanField(default=False)
    canal_cliente = models.ForeignKey(CanalCliente, on_delete=models.CASCADE, default=None, null=True, blank=True)