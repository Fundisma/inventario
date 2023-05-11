
from django.urls import path, include

from core.principal.views import DetalleLibro, DonacionView, EventosView, HistoriaView, libros

app_name = 'principal'

urlpatterns = [
    path('libros/',libros, name= 'libros'),
    # path('search/',search,name="search"),
    # path('biblioteca/',BibliotecaView.as_view(), name='biblioteca'),
    path('detalleLibro/<int:pk>/',  DetalleLibro.as_view(), name='detalleLibro'),
    path('eventos/',EventosView.as_view(), name='eventos'),
    path('historia/',HistoriaView.as_view(), name='historia'),
    path('donaciones/',DonacionView.as_view(), name='donaciones'),
    



]