from django.urls import path
from core.base.views.categoria.views import *
from core.base.views.productos.views import *
from core.base.views.beneficiario.views import *
from core.base.views.suministro.views import *
from core.base.views.admin.views import *


app_name = 'base'

urlpatterns = [
    #categoria
    path ('categoria/',CategoriaView.as_view(), name='categoria_listado'),
    

    #productos
    path('productos/listado/', ProductosListView.as_view(), name='productos_listado'),
    path('productos/add/', ProductosCreateView.as_view(), name='productos_create'),
    path('productos/edit/<int:pk>/', ProductosUpdateView.as_view(), name='productos_editar'),
    path('productos/delete/<int:pk>/', ProductosDeleteView.as_view(), name='productos_eliminar'),
    
    #Beneficiarios
    path('beneficiario/', BeneficiarioView.as_view(), name='beneficiario_listado'),  

    #inicio
    path('admin/', AdminView.as_view(), name='admin'),  

    #Suministro
    path('suministro/listado/', SuministroListView.as_view(), name='suministro_listado'),
    path('suministro/add/', SuministroCreateView.as_view(), name='suministro_create'),
    path('suministro/delete/<int:pk>/', SuministroDeleteView.as_view(), name='suministro_delete'),
    path ('suministro/edit/<int:pk>/',SuministroUpdateView.as_view(), name='suministro_edit'),

    
]