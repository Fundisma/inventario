from django.contrib import admin
from core.base.models import*

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Productos) 
admin.site.register(Beneficiario) 
admin.site.register(Suministro) 
admin.site.register(DetalleSuministro) 

