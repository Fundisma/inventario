
from django.urls import path
from core.base.views.reserva.views import *
from core.base.views.eventos.views import *
from core.base.views.libro.views import *
from core.base.views.autor.views import *
from core.base.views.categoria.views import *
from core.base.views.categoriaLibro.views import *
from core.base.views.productos.views import *
from core.base.views.inventario.views import *
from core.base.views.lector.views import *
from core.base.views.beneficiario.views import *
from core.base.views.suministro.views import *
from core.base.views.admin.views import *

app_name = 'base'

urlpatterns = [

    #Reserva
    path('reserva/listado/',  ReservaListView.as_view(), name='reserva_listado'),
    path('reserva/add/', ReservaCreateView.as_view(), name='reserva_create'),
    path('reserva/edit/<int:pk>/', ReservaUpdateView.as_view(), name='reserva_editar'),
    path('reserva/delete/<int:pk>/', ReservaDeleteView.as_view(), name='reserva_eliminar'),

    #Eventos
    path('eventos/listado/',  EventosListView.as_view(), name='eventos_listado'),
    path('calendar/',  CalendarView.as_view(), name='calendar'),
    path('eventos/add/', EventosCreateView.as_view(), name='eventos_create'),
    path('eventos/edit/<int:pk>/', EventosUpdateView.as_view(), name='eventos_editar'),
    path('eventos/delete/<int:pk>/', EventosDeleteView.as_view(), name='eventos_eliminar'),
    
    #Libro
    path('libro/listado/',  LibroListView.as_view(), name='libro_listado'),
    path('libro/add/', LibroCreateView.as_view(), name='libro_create'),
    path('libro/edit/<int:pk>/', LibroUpdateView.as_view(), name='libro_editar'),
    path('libro/delete/<int:pk>/', LibroDeleteView.as_view(), name='libro_eliminar'),
    path('detalle-libro/pdf/<int:pk>/',  DetalleLibroDisponible.as_view(), name='detalle_libro'),

    #Autor
    path('autor/listado/',  AutorListView.as_view(), name='autor_listado'),
    path('autor/add/', AutorCreateView.as_view(), name='autor_create'),
    path('autor/edit/<int:pk>/', AutorUpdateView.as_view(), name='autor_editar'),
    path('autor/delete/<int:pk>/', AutorDeleteView.as_view(), name='autor_eliminar'),

    #categoria
    path('categoria/listado/',  CategoriaListView.as_view(), name='categoria_listado'),
    path('categoria/add/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/edit/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_eliminar'),

    #categoriaLibro
    path('categoriaLibro/listado/',  CategoriaLibroListView.as_view(), name='categoriaLibro_listado'),
    path('categoriaLibro/add/', CategoriaLibroCreateView.as_view(), name='categoriaLibro_create'),
    path('categoriaLibro/edit/<int:pk>/', CategoriaLibroUpdateView.as_view(), name='categoriaLibro_editar'),
    path('categoriaLibro/delete/<int:pk>/', CategoriaLibroDeleteView.as_view(), name='categoriaLibro_eliminar'),

    #productos
    path('productos/listado/', ProductosListView.as_view(), name='productos_listado'),
    path('productos/add/', ProductosCreateView.as_view(), name='productos_create'),
    path('productos/edit/<int:pk>/', ProductosUpdateView.as_view(), name='productos_editar'),
    path('productos/delete/<int:pk>/', ProductosDeleteView.as_view(), name='productos_eliminar'),

    #inventario
    path('inventario/listado/', InventarioListView.as_view(), name='inventario_listado'),
    path('inventario/add/', InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario/edit/<int:pk>/', InventarioUpdateView.as_view(), name='inventario_editar'),
    path('inventario/delete/<int:pk>/', InventarioDeleteView.as_view(), name='inventario_eliminar'),

    #Beneficiarios
    path('beneficiario/listado/', BeneficiarioListView.as_view(), name='beneficiario_listado'),
    path('beneficiario/add/', BeneficiarioCreateView.as_view(), name='beneficiario_create'),
    path('beneficiario/edit/<int:pk>/', BeneficiarioUpdateView.as_view(), name='beneficiario_editar'),
    path('beneficiario/delete/<int:pk>/', BeneficiarioDeleteView.as_view(), name='beneficiario_eliminar'),

    #inicio admin
    path('admin/', AdminView.as_view(), name='admin'), 
    path('ayuda/',  AyudaView.as_view(), name='ayuda'),

    #Suministro
    path('suministro/listado/', SuministroListView.as_view(), name='suministro_listado'),
    path('suministro/add/', SuministroCreateView.as_view(), name='suministro_create'),
    path('suministro/delete/<int:pk>/', SuministroDeleteView.as_view(), name='suministro_delete'),
    path ('suministro/edit/<int:pk>/',SuministroUpdateView.as_view(), name='suministro_edit'),
    path('suministro/pdf/<int:pk>/',SuministroPdfView.as_view(), name='suministro_pdf'),
    
    #Lector
    path('Lector/listado/', LectorListView.as_view(), name='lector_listado'),
    path('Lector/add/', LectorCreateView.as_view(), name='lector_create'),
    path('Lector/edit/<int:pk>/', LectorUpdateView.as_view(), name='lector_editar'),
    path('Lector/delete/<int:pk>/', LectorDeleteView.as_view(), name='lector_eliminar'),
]