from django import forms 
from .models import *

#LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

#EMPRESAS
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nro_documento', 'razon_social', 'direccion']
        widgets = {
            'nro_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

#SUCURSALES
class SucursalForm(forms.ModelForm):
    empresa_id = forms.ModelChoiceField(queryset=Empresa.objects.all(),
        widget=forms.Select(attrs={'class': 
                                   'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        # Personalizamos la representación de las opciones del campo empresa
        self.fields['empresa_id'].label_from_instance = lambda obj: f"{obj.razon_social}"

    class Meta:
        model = Sucursales
        fields = [ 'nombre_comercial', 'direccion','empresa_id']
        widgets = {
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

#MARCAS
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marcas
        fields = ['codigo_marca', 'marca_nombre']
        widgets = {
            'codigo_marca': forms.TextInput(attrs={'class': 'form-control'}),
            'marca_nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

#UNIDADES DE MEDIDA
class UnidadForm(forms.ModelForm):
    class Meta:
        model = UnidadesMedida
        fields = ['unidad_medida_id','unidad_nombre']
        widgets = {
            'unidad_medida_id': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad_nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ClientesForm(forms.ModelForm):
    tipo_identificacionC_id = forms.ModelChoiceField(queryset=TiposIdentificacion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    canal_cliente_id = forms.ModelChoiceField(queryset=CanalCliente.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Clientes
        fields = ['tipo_identificacionC_id', 'nro_documento', 'nombre_razon_social', 'direccion', 'canal_cliente_id']
        widgets = {
            'nro_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClientesForm, self).__init__(*args, **kwargs)
        
        # Personalizamos la representación de las opciones del campo empresa
        self.fields['tipo_identificacionC_id'].label_from_instance = lambda obj: f"{obj.tipo_identificacion_nombre}"

        # Personalizamos la representación de las opciones del campo responsable_grupo
        self.fields['canal_cliente_id'].label_from_instance = lambda obj: f"{obj.canal_cliente_descripcion}"


#CANAL DE CLIENTE
class CanalClienteForm(forms.ModelForm):
 
    def __init__(self, *args, **kwargs):
        super(CanalClienteForm, self).__init__(*args, **kwargs)
        # Personaliza la representación de las opciones del campo tipo_documento

    class Meta:
        model = CanalCliente
        fields = [ 'canal_cliente_id', 'canal_cliente_descripcion']
        widgets = {
            'canal_cliente_id': forms.TextInput(attrs={'class': 'form-control'}),
            'canal_cliente_descripcion': forms.Select(attrs={'class': 'custom-select'}),
    
        }

#TIPO DE IDENTIFICACION
class TiposIdentificacionForm(forms.ModelForm):
    class Meta:
        model = TiposIdentificacion
        fields = ['tipo_identificacion_id','tipo_identificacion_nombre']
        widgets = {
            'tipo_identificacion_id': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_identificacion_nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

#TIPOS DE PEDIDO
class TiposPedidoForm(forms.ModelForm):
    class Meta:
        model = TiposPedido
        fields = ['tipo_pedido_id','tipo_pedido_nombre']
        widgets = {
            'tipo_pedido_id': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pedido_nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
#CONDICIONES DE VENTA
class CondicionesVentaForm(forms.ModelForm):
    class Meta:
        model = CondicionesVenta
        fields = ['condicion_venta','descripcion','genera_credito']
        widgets = {
            'condicion_venta': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'genera_credito': forms.TextInput(attrs={'class': 'form-control'}),
        }

#VENTAS
class NotasVentaForm(forms.ModelForm):
    class Meta:
        model = NotasVenta
        fields = [
            'empresa_id',
            'sucursal_id',
            'tipo_pedido_id',
            'cliente_id',
            'condicion_venta',
            'plazo',
            'tipo_documento',
        ]
        widgets = {
            'empresa_id': forms.Select(attrs={'class': 'form-control'}),
            'sucursal_id': forms.Select(attrs={'class': 'form-control'}),
            'tipo_pedido_id': forms.Select(attrs={'class': 'form-control'}),
            'cliente_id': forms.Select(attrs={'class': 'form-control'}),
            'condicion_venta': forms.Select(attrs={'class': 'form-control'}),
            'plazo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.TextInput(attrs={'class': 'form-control'}),
        }

#PROMOCIONES
class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promociones
        fields = ['fecha_inicio','fecha_fin','descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

#DETALLE DE FORMULA
class FormulaForm(forms.ModelForm):
    promocion_id = forms.ModelChoiceField(queryset=Promociones.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = FormulaDetalle
        fields = ['tipoPromocion','descripcion','promocion_id', 'formula']
        widgets = {
            'tipoPromocion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'formula': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(FormulaForm, self).__init__(*args, **kwargs)
        # Personalizamos la representación de las opciones del campo empresa
        self.fields['promocion_id'].label_from_instance = lambda obj: f"{obj.descripcion}"

#ARTICULOS    
class ArticulosForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields = ['codigo_sku', 'descripcion', 'unidad_medida_id', 'grupo_id', 'precio_unitario', 'linea_id', 'sublinea_id', 'empresa_id', 'factor_compra', 'factor_reparto', 'marca_id']

        widgets = {
            'codigo_sku': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad_medida_id': forms.Select(attrs={'class': 'form-control'}),
            'grupo_id': forms.Select(attrs={'class': 'form-control'}),
            'precio_unitario': forms.TextInput(attrs={'class': 'form-control'}),
            'linea_id': forms.Select(attrs={'class': 'form-control'}),
            'sublinea_id': forms.Select(attrs={'class': 'form-control'}),
            'empresa_id': forms.Select(attrs={'class': 'form-control'}),
            'factor_compra': forms.TextInput(attrs={'class': 'form-control'}),
            'factor_reparto': forms.TextInput(attrs={'class': 'form-control'}),
            'marca_id': forms.Select(attrs={'class': 'form-control'}),
        }     
#ItemsNotaVenta
class ItemsNotaVentaForm(forms.ModelForm):
    class Meta:
        model = ItemsNotaVenta
        fields = ['articulo_id', 'cantidad']

        widgets = {
            'articulo_id': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
        }


#GruposProveedor   
class GruposProveedorForm(forms.ModelForm):
    empresa_id = forms.ModelChoiceField(queryset=Empresa.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    responsable_grupo = forms.ModelChoiceField(queryset=Usuario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = GruposProveedor
        fields = [ 'codigo_grupo', 'grupo_descripcion', 'empresa_id', 'activo','responsable_grupo']
        widgets = {
            'codigo_grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo_descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(GruposProveedorForm, self).__init__(*args, **kwargs)
        
        # Personalizamos la representación de las opciones del campo empresa
        self.fields['empresa_id'].label_from_instance = lambda obj: f"{obj.razon_social}"

        # Personalizamos la representación de las opciones del campo responsable_grupo
        self.fields['responsable_grupo'].label_from_instance = lambda obj: f"{obj.fullname}"

#LineasArticulos
class LineasArticulosForm(forms.ModelForm):
    grupo_id = forms.ModelChoiceField(queryset=GruposProveedor.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    responsable_linea= forms.ModelChoiceField(queryset=Usuario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = LineasArticulos
        fields = ['codigo_linea', 'linea_descripcion', 'grupo_id', 'activo', 'responsable_linea']
        widgets = {
            'codigo_linea': forms.TextInput(attrs={'class': 'form-control'}),
            'linea_descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(LineasArticulosForm, self).__init__(*args, **kwargs)
        
        # Personalizamos la representación de las opciones del campo empresa
        self.fields['grupo_id'].label_from_instance = lambda obj: f"{obj.codigo_grupo}"

        # Personalizamos la representación de las opciones del campo responsable_grupo
        self.fields['responsable_linea'].label_from_instance = lambda obj: f"{obj.fullname}"

#SubLineasArticulos
class SublineasArticulosForm(forms.ModelForm):
    linea_id = forms.ModelChoiceField(queryset=LineasArticulos.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SublineasArticulos
        fields = ['codigo_sublinea', 'sublinea_descripcion', 'linea_id', 'estado']
        widgets = {
            'codigo_sublinea': forms.TextInput(attrs={'class': 'form-control'}),
            'sublinea_descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(SublineasArticulosForm, self).__init__(*args, **kwargs)
        
        # Personalizamos la representación de las opciones del campo linea
        self.fields['linea_id'].label_from_instance = lambda obj: f"{obj.codigo_linea}"