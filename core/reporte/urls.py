from django.urls import path
from core.reporte.views import ReporteSuministroView

urlpatterns = [
    #reportes
    path('suministro/', ReporteSuministroView.as_view(), name='suministro_reporte'), 


]