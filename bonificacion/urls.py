from django.urls import include, path
from django.contrib.auth.decorators import login_required
from bonificacion.views import *

urlpatterns = [
    path('', login_user, name='login'),
    path('inicio', login_required(index), name='index'),  # Ruta de inicio protegida     
    path('logout',logout_user, name='logout'),

    #EMPRESAS
    path('listarEmpresas/', login_required(EmpresaListView.as_view()), name='empresa_list'),
    path('crearEmpresas/', login_required(EmpresaCreateView.as_view()), name='empresa_create'),
    path('<uuid:pk>/editarEmpresa/', login_required(EmpresaUpdateView.as_view()), name='empresa_update'),
    path('<uuid:pk>/eliminarEmpresa/', login_required(EmpresaDeleteView.as_view()), name='empresa_delete'),

    #SUCURSALES
    path('listarSucursales/', login_required(SucursalListView.as_view()), name='sucursal_list'),
    path('crearSucursal/', login_required(SucursalCreateView.as_view()), name='sucursal_create'),
    path('<uuid:pk>/editarSucursal/', login_required(SucursalUpdateView.as_view()), name='sucursal_update'),
    path('<uuid:pk>/eliminarSucursal/', login_required(SucursalDeleteView.as_view()), name='sucursal_delete'),

    #MARCAS
    path('listarMarcas/', login_required(MarcaListView.as_view()), name='marca_list'),
    path('crearMarca/', login_required(MarcaCreateView.as_view()), name='marca_create'),
    path('<uuid:pk>/editarMarca/', login_required(MarcaUpdateView.as_view()), name='marca_update'),
    path('<uuid:pk>/eliminarMarca/', login_required(MarcaDeleteView.as_view()), name='marca_delete'),

    #UNIDADES DE MEDIDA
    path('listarUnidades/', login_required(UnidadListView.as_view()), name='unidad_list'),
    path('crearUnidad/', login_required(UnidadCreateView.as_view()), name='unidad_create'),
    path('<str:pk>/editarUnidad/', login_required(UnidadUpdateView.as_view()), name='unidad_update'),
    path('<str:pk>/eliminarUnidad/', login_required(UnidadDeleteView.as_view()), name='unidad_delete'),

    #CLIENTES
    path('listarClientes/',login_required(ClienteListView.as_view()), name='cliente_list'),
    path('crearCliente/',login_required( ClienteCreateView.as_view()), name='cliente_create'),
    path('<uuid:pk>/editarCliente/', login_required(ClienteUpdateView.as_view()), name='cliente_update'),
    path('<uuid:pk>/eliminarCliente/', login_required( ClienteDeleteView.as_view()), name='cliente_delete'),
    
    #CANAL CLIENTE
    path('listarCa/', login_required(CanalClienteListView.as_view()), name='canalcliente_list'),
    path('crearCa/', login_required(CanalClienteCreateView.as_view()), name='canalcliente_create'),
    path('<str:pk>/editarCa/', login_required(CanalClienteUpdateView.as_view()), name='canalcliente_update'),
    path('<str:pk>/eliminarCa/', login_required(CanalClienteDeleteView.as_view()), name='canalcliente_delete'),
    
    #TIPO DE IDENTIFICACION
    path('listarIdentificaciones/', login_required(TiposIdentificacionListView.as_view()), name='tiposidentificacion_list'),
    path('crearIdentificacion/', login_required(TiposIdentificacionCreateView.as_view()), name='tiposidentificacion_create'),
    path('<str:pk>/editarIdentificacion/', login_required(TiposIdentificacionUpdateView.as_view()), name='tiposidentificacion_update'),
    path('<str:pk>/eliminarIdentificacion/', login_required(TiposIdentificacionDeleteView.as_view()), name='tiposidentificacion_delete'),

    #TIPOS DE PEDIDO
    path('listarPe/', login_required(TiposPedidoListView.as_view()), name='tipopedido_list'),
    path('crearPe/', login_required(TiposPedidoCreateView.as_view()), name='tipopedido_create'),
    path('<str:pk>/editarPe/', login_required(TiposPedidoUpdateView.as_view()), name='tipopedido_update'),
    path('<str:pk>/eliminarPe/', login_required(TiposPedidoDeleteView.as_view()), name='tipopedido_delete'),
    
    #CONDICIONES DE VENTA
    path('listarCVe/', login_required(CondicionesVentaListView.as_view()), name='condicionventa_list'),
    path('crearCVe/', login_required(CondicionesVentaCreateView.as_view()), name='condicionventa_create'),
    path('<str:pk>/editarCVe/', login_required(CondicionesVentaUpdateView.as_view()), name='condicionventa_update'),
    path('<str:pk>/eliminarCVe/', login_required(CondicionesVentaDeleteView.as_view()), name='condicionventa_delete'),    

    #VENTAS
    path('listarVentas/', login_required(NotasVentaListView.as_view()), name='venta_list'),
    path('crearVenta/', login_required(NotasVentaCreateView.as_view()), name='venta_create'),
    path('<uuid:pk>/editarVenta/', login_required(NotasVentaUpdateView.as_view()), name='venta_update'),
    path('<uuid:pk>/eliminarVenta/', login_required(NotasVentaDeleteView.as_view()), name='venta_delete'),

    #PROMOCIONES
    path('listarPromociones/', login_required(PromocionesListView.as_view()), name='promocion_list'),
    path('crearPromocion/', login_required(PromocionesCreateView.as_view()), name='promocion_create'),
    path('<uuid:pk>/editarPromocion/', login_required(PromocionesUpdateView.as_view()), name='promocion_update'),
    path('<uuid:pk>/eliminarPromocion/', login_required(PromocionesDeleteView.as_view()), name='promocion_delete'),

    #DETALLE DE FORMULA
    path('listarFormulas/', login_required(FormulasListView.as_view()), name='formuladetalle_list'),
    path('crearFormula/', login_required(FormulasCreateView.as_view()), name='formuladetalle_create'),
    path('<uuid:pk>/editarFormula/', login_required(FormulasUpdateView.as_view()), name='formuladetalle_update'),
    path('<uuid:pk>/eliminarFormula/', login_required(FormulasDeleteView.as_view()), name='formuladetalle_delete'),
    
    #ItemsNotaVenta
    path('listarItem/', login_required(ItemsNotaVentaListView.as_view()), name='itemsnotaventa_list'),
     path('crearItem/<uuid:nota_venta_id>/', login_required(ItemsNotaVentaCreateView.as_view()), name='itemsnotaventa_create'),
    path('<uuid:pk>/editarItem/', login_required(ItemsNotaVentaUpdateView.as_view()), name='itemsnotaventa_update'),
    # path('<uuid:pk>/eliminarItem/', login_required(ItemsNotaVentaDeleteView.as_view()), name='itemsnotaventa_delete'),
   
    #ARTICULO
    path('listarArt/', login_required(ArticulosListView.as_view()), name='articulos_list'),
    path('crearArt/', login_required(ArticulosCreateView.as_view()), name='articulos_create'),
    path('<uuid:pk>/editarArt/', login_required(ArticulosUpdateView.as_view()), name='articulos_update'),
    path('<uuid:pk>/eliminarArt/', login_required(ArticulosDeleteView.as_view()), name='articulos_delete'),

    #GrupoProveedor
    path('listarGP/', login_required(GruposProveedorListView.as_view()), name='grupo_list'),
    path('crearGP/', login_required(GruposProveedorCreateView.as_view()), name='grupo_create'),
    path('<uuid:pk>/editarGP/', login_required(GruposProveedorUpdateView.as_view()), name='grupo_update'),
    path('<uuid:pk>/eliminarGP/', login_required(GruposProveedorDeleteView.as_view()), name='grupo_delete'),
 
    #LineasArticulos
    path('listarLA/', login_required(LineasArticulosListView.as_view()), name='linea_list'),
    path('crearLA/', login_required(LineasArticulosCreateView.as_view()), name='linea_create'),
    path('<uuid:pk>/editarLA/', login_required(LineasArticulosUpdateView.as_view()), name='linea_update'),
    path('<uuid:pk>/eliminarLA/', login_required(LineasArticulosDeleteView.as_view()), name='linea_delete'),

   #SubLineasArticulos
    path('listarSLA/', login_required(SublineasArticulosListView.as_view()), name='sublinea_list'),
    path('crearSLA/', login_required(SublineasArticulosCreateView.as_view()), name='sublinea_create'),
    path('<uuid:pk>/editarSLA/', login_required(SublineasArticulosUpdateView.as_view()), name='sublinea_update'),
    path('<uuid:pk>/eliminarSLA/', login_required(SublineasArticulosDeleteView.as_view()), name='sublinea_delete'),

    #DESCUENTOS
    path('listarDescuentos/', login_required(DescuentosListView.as_view()), name='descuento_list'),
    path('crearDescuento/', login_required(DescuentosCreateView.as_view()), name='descuento_create'),
    path('<uuid:pk>/editarDescuento/', login_required(DescuentosUpdateView.as_view()), name='descuento_update'),
    path('<uuid:pk>/eliminarDescuento/', login_required(DescuentosDeleteView.as_view()), name='descuento_delete'),
    
]