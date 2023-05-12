from django.contrib import admin
from core.base.forms import ReservaForm
from core.base.models import*

class ReservaAdmin(admin.ModelAdmin):
    form = ReservaForm
# Register your models here.
admin.site.register(Lector)
admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Eventos)
admin.site.register(Reserva,ReservaAdmin)
admin.site.register(Categoria)
admin.site.register(categoriaLibro)
admin.site.register(Productos) 
admin.site.register(inventario) 
admin.site.register(Beneficiario) 
admin.site.register(Suministro) 
admin.site.register(DetalleSuministro) 

