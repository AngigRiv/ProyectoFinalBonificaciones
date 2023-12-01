import json
from django.views.generic.edit import FormView
from msilib.schema import *
from django.http import JsonResponse
from django.views.generic import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Crea una instancia del formulario con los datos POST
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Contraseña o correo incorrectos.')
        else:
            messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')

    else:
        # El formulario de autenticación maneja automáticamente las credenciales incorrectas
        # Sin embargo, puedes mostrar un mensaje de error personalizado si lo deseas.
        form = LoginForm()  # Si es una solicitud GET, crea un formulario en blanco
    return render(request, 'plantilla/login.html', {'form': form})

def index(request):
    return render(request,'inicio.html')

def logout_user(request):
    logout(request)
    return redirect('login')

#EMPRESA
class EmpresaListView(ListView):
    model = Empresa
    template_name = 'empresa/empresa_list.html'  # Crea un archivo HTML para listar las marcas

class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/empresa_form.html'  # Crea un archivo HTML para el formulario de creación
    success_url = reverse_lazy('empresa_list')  # Redirige a la lista de marcas después de crear una marca

class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/empresa_form.html'  # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('empresa_list')  # Redirige a la lista de marcas después de actualizar una marca

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'empresa/empresa_confirm_delete.html'  # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('empresa_list')  # Redirige a la lista de marcas después de eliminar una marca

#SUCURSAL
# Vista para listar las sucursales
class SucursalListView(ListView):
    model = Sucursales
    template_name = 'sucursal/sucursal_list.html'
    context_object_name = 'sucursales'

    def get_queryset(self):
        # Modificamos la consulta para incluir la razón social de la empresa
        return Sucursales.objects.select_related('empresa_id')
    
# Vista para crear una nueva sucursal
class SucursalCreateView(CreateView):
    model = Sucursales
    form_class = SucursalForm
    template_name = 'sucursal/sucursal_form.html'
    success_url = reverse_lazy('sucursal_list')

# Vista para editar una sucursal existente
class SucursalUpdateView(UpdateView):
    model = Sucursales
    form_class = SucursalForm
    template_name = 'sucursal/sucursal_form.html'
    success_url = reverse_lazy('sucursal_list')

# Vista para eliminar una sucursal
class SucursalDeleteView(DeleteView):
    model = Sucursales
    template_name = 'sucursal/sucursal_confirm_delete.html'
    success_url = reverse_lazy('sucursal_list')

#MARCA
class MarcaListView(ListView):
    model = Marcas
    template_name = 'marca/marca_list.html'  # Crea un archivo HTML para listar las marcas

class MarcaCreateView(CreateView):
    model = Marcas
    form_class = MarcaForm
    template_name = 'marca/marca_form.html'  # Crea un archivo HTML para el formulario de creación
    success_url = reverse_lazy('marca_list')  # Redirige a la lista de marcas después de crear una marca

class MarcaUpdateView(UpdateView):
    model = Marcas
    form_class = MarcaForm
    template_name = 'marca/marca_form.html'  # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('marca_list')  # Redirige a la lista de marcas después de actualizar una marca

class MarcaDeleteView(DeleteView):
    model = Marcas
    template_name = 'marca/marca_confirm_delete.html'  # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('marca_list')  # Redirige a la lista de marcas después de eliminar una marca

#UNIDADES DE MEDIDA
class UnidadListView(ListView):
    model = UnidadesMedida
    template_name = 'unidad/unidad_list.html'  # Crea un archivo HTML para listar las marcas
   

class UnidadCreateView(CreateView):
    model = UnidadesMedida
    form_class = UnidadForm
    template_name = 'unidad/unidad_form.html'  # Crea un archivo HTML para el formulario de creación
    success_url = reverse_lazy('unidad_list')  # Redirige a la lista de marcas después de crear una marca

class UnidadUpdateView(UpdateView):
    model = UnidadesMedida
    form_class = UnidadForm
    template_name = 'unidad/unidad_form.html'  # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('unidad_list')  # Redirige a la lista de marcas después de actualizar una marca

class UnidadDeleteView(DeleteView):
    model = UnidadesMedida
    template_name = 'unidad/unidad_confirm_delete.html'  # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('unidad_list')  # Redirige a la lista de marcas después de eliminar una marca

#CANAL DE CLIENTE
class CanalClienteListView(ListView):
    model = CanalCliente
    template_name = 'canalcliente/canalcliente_list.html'
    context_object_name = 'CanalCliente'

# Vista para crear un nueva personal
class CanalClienteCreateView(CreateView):
    model = CanalCliente
    form_class = CanalClienteForm
    template_name = 'canalcliente/canalcliente_form.html'
    success_url = reverse_lazy('canalcliente_list')

class CanalClienteUpdateView(UpdateView):
    model = CanalCliente
    form_class = CanalClienteForm
    template_name = 'canalcliente/canalcliente_form.html'  # Corrige esta línea
    success_url = reverse_lazy('canalcliente_list')

# Vista para eliminar unn personal
class CanalClienteDeleteView(DeleteView):
    model = CanalCliente
    template_name = 'canalcliente/canalcliente_confirm_delete.html'
    success_url = reverse_lazy('canalcliente_list')
    
#CLIENTE
class ClienteListView(ListView):
    model = Clientes
    template_name = 'cliente/cliente_list.html'  # Crea un archivo HTML para listar los grupos proveedor

    def get_queryset(self):
        # Modificamos la consulta para incluir la razón social de la empresa
        return Clientes.objects.select_related('tipo_identificacionC_id')
    
    def get_queryset(self):
        # Modificamos la consulta para incluir nombre del personal
        return Clientes.objects.select_related('canal_cliente_id')

class ClienteCreateView(CreateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'cliente/cliente_form.html'  # Crea un archivo HTML para el formulario de creación
    success_url = reverse_lazy('cliente_list')  # Redirige a la lista de marcas después de crear una marca

class ClienteUpdateView(UpdateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'cliente/cliente_form.html'  # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('cliente_list')  # Redirige a la lista de marcas después de actualizar una marca

class ClienteDeleteView(DeleteView):
    model = Clientes
    template_name = 'cliente/cliente_confirm_delete.html'  # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('cliente_list')  # Redirige a la lista de marcas después de eliminar una marca

#TIPO DE IDENTIFICACION
class TiposIdentificacionListView(ListView):
    model = TiposIdentificacion
    template_name = 'tiposidentificacion/tiposidentificacion_list.html' 
   
class TiposIdentificacionCreateView(CreateView):
    model = TiposIdentificacion
    form_class = TiposIdentificacionForm
    template_name = 'tiposidentificacion/tiposidentificacion_form.html'
    success_url = reverse_lazy('tiposidentificacion_list')  
    
class TiposIdentificacionUpdateView(UpdateView):
    model = TiposIdentificacion
    form_class = TiposIdentificacionForm
    template_name = 'tiposidentificacion/tiposidentificacion_form.html'  
    success_url = reverse_lazy('tiposidentificacion_list')  

class TiposIdentificacionDeleteView(DeleteView):
    model = TiposIdentificacion
    template_name = 'tiposidentificacion/tiposidentificacion_confirm_delete.html'  
    success_url = reverse_lazy('tiposidentificacion_list')  

#TIPOS DE PEDIDO
class TiposPedidoListView(ListView):
    model = TiposPedido
    template_name = 'tipopedido/tipopedido_list.html' 
   
class TiposPedidoCreateView(CreateView):
    model = TiposPedido
    form_class = TiposPedidoForm
    template_name = 'tipopedido/tipopedido_form.html'
    success_url = reverse_lazy('tipopedido_list')  
class TiposPedidoUpdateView(UpdateView):
    model = TiposPedido
    form_class = TiposPedidoForm
    template_name = 'tipopedido/tipopedido_form.html'  
    success_url = reverse_lazy('tipopedido_list')  

class TiposPedidoDeleteView(DeleteView):
    model = TiposPedido
    template_name = 'tipopedido/tipopedido_confirm_delete.html'  
    success_url = reverse_lazy('tipopedido_list')  
    
#CONDICIONES DE VENTA
class CondicionesVentaListView(ListView):
    model = CondicionesVenta
    template_name = 'condicionventa/condicionventa_list.html'
    context_object_name = 'object_list'  # Agrega esta línea

class CondicionesVentaCreateView(CreateView):
    model = CondicionesVenta
    form_class = CondicionesVentaForm
    template_name = 'condicionventa/condicionventa_form.html'
    success_url = reverse_lazy('condicionventa_list')  

class CondicionesVentaUpdateView(UpdateView):
    model = CondicionesVenta
    form_class = CondicionesVentaForm
    template_name = 'condicionventa/condicionventa_form.html'  
    success_url = reverse_lazy('condicionventa_list')  

class CondicionesVentaDeleteView(DeleteView):
    model = CondicionesVenta
    template_name = 'condicionventa/condicionventa_confirm_delete.html'  
    success_url = reverse_lazy('condicionventa_list')     

#VENTAS
class NotasVentaListView(ListView):
    model = NotasVenta
    template_name = 'venta/venta_list.html'  # Crea un archivo HTML para listar las marcas
   

class NotasVentaCreateView(CreateView):
    model = NotasVenta
    form_class = NotasVentaForm
    template_name = 'venta/venta_form.html'
    success_url = reverse_lazy('detalle_venta_create')


class NotasVentaUpdateView(UpdateView):
    model = NotasVenta
    form_class = NotasVentaForm
    template_name = 'venta/venta_update_form.html'  # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('venta_list')  # Redirige a la lista de marcas después de actualizar una marca

class NotasVentaDeleteView(DeleteView):
    model = NotasVenta
    template_name = 'venta/venta_confirm_delete.html'  # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('venta_list')  # Redirige a la lista de marcas después de eliminar una marca

#PROMOCIONES
class PromocionesListView(ListView):
    model = Promociones
    template_name = 'promocion/promocion_list.html'  # Crea un archivo HTML para listar las marcas
   
class PromocionesCreateView(CreateView):
    model = Promociones
    form_class = PromocionForm
    template_name = 'promocion/promocion_form.html' 
    success_url = reverse_lazy('promocion_list') 

class PromocionesUpdateView(UpdateView):
    model = Promociones
    form_class = PromocionForm
    template_name = 'promocion/promocion_form.html'
    success_url = reverse_lazy('promocion_list')

class PromocionesDeleteView(DeleteView):
    model = Promociones
    template_name = 'promocion/promocion_confirm_delete.html'
    success_url = reverse_lazy('promocion_list')

#DETALLE DE FORMULA
class FormulasListView(ListView):
    model = FormulaDetalle
    template_name = 'formuladetalle/formuladetalle_list.html'  # Crea un archivo HTML para listar las marcas
   

class FormulasCreateView(CreateView):
    model = FormulaDetalle
    form_class = FormulaForm
    template_name = 'formuladetalle/formuladetalle_form.html' 
    success_url = reverse_lazy('formuladetalle_list') 

class FormulasUpdateView(UpdateView):
    model = FormulaDetalle
    form_class = FormulaForm
    template_name = 'formuladetalle/formuladetalle_form.html'
    success_url = reverse_lazy('formuladetalle_list')

class FormulasDeleteView(DeleteView):
    model = FormulaDetalle
    template_name = 'formuladetalle/formuladetalle_confirm_delete.html'
    success_url = reverse_lazy('formuladetalle_list')
 
 #ARTICULOS
class ArticulosListView(ListView):
    model = Articulos
    template_name = 'articulos/articulos_list.html'  # Crea un archivo HTML para listar las marcas
   
class ArticulosCreateView(CreateView):
    model = Articulos
    form_class = ArticulosForm
    template_name = 'articulos/articulos_form.html'  # Crea un archivo HTML para el formulario de creación
    success_url = reverse_lazy('articulos_list')  # Redirige a la lista de marcas después de crear una marca

class ArticulosUpdateView(UpdateView):
    model = Articulos
    form_class = ArticulosForm
    template_name = 'articulos/articulos_form.html'  # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('articulos_list')  # Redirige a la lista de marcas después de actualizar una marca

class ArticulosDeleteView(DeleteView):
    model = Articulos
    template_name = 'articulos/articulos_confirm_delete.html'  # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('articulos_list')  # Redirige a la lista de marcas después de eliminar una marca
   
#ItemsNotaVenta
class ItemsNotaVentaListView(ListView):
    model = ItemsNotaVenta
    template_name = 'itemsnotaventa/itemsnotaventa_list.html'  # Crea un archivo HTML para listar las marcas
   
# class ItemsNotaVentaCreateView(CreateView):
#     model = ItemsNotaVenta
#     form_class = ItemsNotaVentaForm
#     template_name = 'itemsnotaventa/itemsnotaventa_form.html'  # Crea un archivo HTML para el formulario de creación
#     success_url = reverse_lazy('itemsnotaventa_list')  # Redirige a la lista de marcas después de crear una marca

class ItemsNotaVentaCreateView(FormView, ListView):
    template_name = 'itemsnotaventa/itemsnotaventa_form.html'
    form_class = ItemsNotaVentaForm

    def get(self, request, *args, **kwargs):
        nota_venta_id = kwargs['nota_venta_id']
        self.initial['nota_venta_id'] = nota_venta_id
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Procesar el formulario y luego redirigir a la misma página
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige a la misma página después de procesar el formulario
        return self.request.path

    def get_queryset(self):
        # Obtén la lista de items asociados a la nota de venta actual
        nota_venta_id = self.kwargs['nota_venta_id']
        return ItemsNotaVenta.objects.filter(nota_venta_id=nota_venta_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega el formulario al contexto
        context['form'] = self.get_form()
        return context  # Reemplaza con la URL real
    
class ItemsNotaVentaUpdateView(UpdateView):
    model = ItemsNotaVenta
    form_class = ItemsNotaVentaForm
    template_name = 'itemsnotaventa/itemsnotaventa_form.html'  # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('itemsnotaventa_list')  # Redirige a la lista de marcas después de actualizar una marca

class ItemsNotaVentaDeleteView(DeleteView):
    model = ItemsNotaVenta
    template_name = 'itemsnotaventa/itemsnotaventa_confirm_delete.html'  # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('itemsnotaventa_list')  # Redirige a la lista de marcas después de eliminar una marca

#GrupoProveedor
class GruposProveedorListView(ListView):
    model = GruposProveedor
    template_name = 'grupo/grupo_list.html'  # Crea un archivo HTML para listar los grupos proveedor
    context_object_name = 'grupos'

    def get_queryset(self):
        # Modificamos la consulta para incluir la razón social de la empresa
        return GruposProveedor.objects.select_related('empresa_id')
    
    def get_queryset(self):
        # Modificamos la consulta para incluir nombre del personal
        return GruposProveedor.objects.select_related('responsable_grupo')

class GruposProveedorCreateView(CreateView):
    model = GruposProveedor
    form_class = GruposProveedorForm
    template_name = 'grupo/grupo_form.html'  # Crea un archivo HTML para el formulario de creación
    success_url = reverse_lazy('grupo_list')  # Redirige a la lista de grupos proveedor después de crear uno

class GruposProveedorUpdateView(UpdateView):
    model = GruposProveedor
    form_class = GruposProveedorForm
    template_name = 'grupo/grupo_form.html'   # Crea un archivo HTML para el formulario de actualización
    success_url = reverse_lazy('grupo_list')  # Redirige a la lista de grupos proveedor después de actualizar uno

class GruposProveedorDeleteView(DeleteView):
    model = GruposProveedor
    template_name = 'grupo/grupo_confirm_delete.html' # Crea un archivo HTML para confirmar la eliminación
    success_url = reverse_lazy('grupo_list')
    
#LineasArticulos
class LineasArticulosListView(ListView):
    model = LineasArticulos
    template_name = 'linea/linea_list.html'
    context_object_name = 'lineas'  # Opcional: Cambia el nombre del objeto en la plantilla

    def get_queryset(self):
        return LineasArticulos.objects.select_related('grupo_id')
    
    def get_queryset(self):
        # Modificamos la consulta para incluir nombre del personal
        return LineasArticulos.objects.select_related('responsable_linea')

class LineasArticulosCreateView(CreateView):
    model = LineasArticulos
    form_class = LineasArticulosForm
    template_name = 'linea/linea_form.html'
    success_url = reverse_lazy('linea_list')

class LineasArticulosUpdateView(UpdateView):
    model = LineasArticulos
    form_class = LineasArticulosForm
    template_name = 'linea/linea_form.html'
    success_url = reverse_lazy('linea_list')

class LineasArticulosDeleteView(DeleteView):
    model = LineasArticulos
    template_name = 'linea/linea_confirm_delete.html'
    success_url = reverse_lazy('linea_list')

#SubLineasArticulos
class SublineasArticulosListView(ListView):
    model = SublineasArticulos
    template_name = 'sublinea/sublinea_list.html'
    context_object_name = 'sublineas'  # Opcional: Cambia el nombre del objeto en la plantilla

    def get_queryset(self):
        return SublineasArticulos.objects.select_related('linea_id')

class SublineasArticulosCreateView(CreateView):
    model = SublineasArticulos
    form_class = SublineasArticulosForm
    template_name = 'sublinea/sublinea_form.html'
    success_url = reverse_lazy('sublinea_list')

class SublineasArticulosUpdateView(UpdateView):
    model = SublineasArticulos
    form_class = SublineasArticulosForm
    template_name = 'sublinea/sublinea_form.html'
    success_url = reverse_lazy('sublinea_list')

class SublineasArticulosDeleteView(DeleteView):
    model = SublineasArticulos
    template_name = 'sublinea/sublinea_confirm_delete.html'
    success_url = reverse_lazy('sublinea_list')