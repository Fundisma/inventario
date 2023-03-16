from django.urls import path
from core.base.views.libro.views import *
from core.base.views.autor.views import *
from core.base.views.categoria.views import *
from core.base.views.productos.views import *
from core.base.views.beneficiario.views import *
from core.base.views.suministro.views import *
from core.base.views.admin.views import *

app_name = 'base'

urlpatterns = [
    #Libro
    path('libro/listado/',  LibroListView.as_view(), name='libro_listado'),
    path('libro/add/', LibroCreateView.as_view(), name='libro_create'),
    path('libro/edit/<int:pk>/', LibroUpdateView.as_view(), name='libro_editar'),
    path('libro/delete/<int:pk>/', LibroDeleteView.as_view(), name='libro_eliminar'),
    path('reservas/', Reservas.as_view(), name='reservas'),
    path('reservas-vencidas/', ReservasVencidas.as_view(), name='reservas_vencidas'),
    path('libros-disponibles/',  ListadoLibrosDisponibles.as_view(), name='libros_disponibles'),
    path('libros-disponibles/',  ListadoLibrosDisponibles.as_view(), name='libros_disponibles'),
    path('listado-reservas-vencidas/',ListadoReservasVencidas.as_view(), name = 'listado_reservas_vencidas'),
    path('detalle-libro/<int:pk>/',  DetalleLibroDisponible.as_view(), name='detalle_libro'),
    path('reservar-libro/',  RegistrarReserva.as_view(), name='reservar_libro'),
    path('libros-reservados/', listadoLibrosReservados.as_view(), name='libros_reservados'),

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

    #productos
    path('productos/listado/', ProductosListView.as_view(), name='productos_listado'),
    path('productos/add/', ProductosCreateView.as_view(), name='productos_create'),
    path('productos/edit/<int:pk>/', ProductosUpdateView.as_view(), name='productos_editar'),
    path('productos/delete/<int:pk>/', ProductosDeleteView.as_view(), name='productos_eliminar'),

    #Beneficiarios
    path('beneficiario/listado/', BeneficiarioListView.as_view(), name='beneficiario_listado'),
    path('beneficiario/add/', BeneficiarioCreateView.as_view(), name='beneficiario_create'),
    path('beneficiario/edit/<int:pk>/', BeneficiarioUpdateView.as_view(), name='beneficiario_editar'),
    path('beneficiario/delete/<int:pk>/', BeneficiarioDeleteView.as_view(), name='beneficiario_eliminar'),

    #inicio admin
    path('admin/', AdminView.as_view(), name='admin'), 

    #Suministro
    path('suministro/listado/', SuministroListView.as_view(), name='suministro_listado'),
    path('suministro/add/', SuministroCreateView.as_view(), name='suministro_create'),
    path('suministro/delete/<int:pk>/', SuministroDeleteView.as_view(), name='suministro_delete'),
    path ('suministro/edit/<int:pk>/',SuministroUpdateView.as_view(), name='suministro_edit'),
    path('suministro/pdf/<int:pk>/',SuministroPdfView.as_view(), name='suministro_pdf'),
    
]