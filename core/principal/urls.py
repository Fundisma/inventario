from django.urls import path, include

from core.principal.views import BibliotecaView, DetalleLibro, EventosView

app_name = 'principal'

urlpatterns = [
    path('biblioteca/',BibliotecaView.as_view(), name='biblioteca'),
    path('detalleLibro/<int:pk>/',  DetalleLibro.as_view(), name='detalleLibro'),
    path('eventos/',EventosView.as_view(), name='eventos'),


]