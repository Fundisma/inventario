from django.urls import path, include

from core.principal.views import EventosView

app_name = 'principal'

urlpatterns = [
    path('eventos/',EventosView.as_view(), name='eventos'),

]