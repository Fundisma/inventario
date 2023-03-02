import json
from django.db import transaction

from django.http import JsonResponse
from django.urls import reverse_lazy

from core.base.forms import SuministroForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from core.base.models import DetalleSuministro, Suministro, Productos
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt

class SuministroListView(ListView):
    model = Suministro
    template_name = 'suministro/listado.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Suministro.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_producto':
                data = []
                for i in DetalleSuministro.objects.filter(suministro_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Suministros'
        context['create_url'] = reverse_lazy('base:suministro_create')
        context['list_url'] = reverse_lazy('base:suministro_listado')
        context['entidad'] = 'Suministro'
        return context


class SuministroCreateView(CreateView):
    model = Suministro
    form_class = SuministroForm
    template_name = 'suministro/create.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_producto':
                data = []
                producto = Productos.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in producto:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action  == 'add':
                with transaction.atomic():
                    suministro = json.loads(request.POST['suministro'])
                    sum = Suministro()
                    sum.fecha_registro = suministro['fecha_registro']
                    sum.beneficiario_id = suministro['beneficiario']
                    sum.subtotal = float(suministro['subtotal'])
                    sum.total = float(suministro['total'])
                    sum.save()
                      
                    for i in suministro['producto']:
                        det = DetalleSuministro()
                        det.suministro_id = sum.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Suministro'
        context['entity'] = 'Suministro'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
    
class SuministroUpdateView(UpdateView):
    model = Suministro
    form_class = SuministroForm
    template_name = 'suministro/create.html'
    success_url = reverse_lazy('base:suministro_listado')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_producto':
                data = []
                producto = Productos.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in producto:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action  == 'edit':
                with transaction.atomic():
                    suministro = json.loads(request.POST['suministro'])
                    sum = self.get_object()
                    sum.fecha_registro = suministro['fecha_registro']
                    sum.beneficiario_id = suministro['beneficiario']
                    sum.subtotal = float(suministro['subtotal'])
                    sum.total = float(suministro['total'])
                    sum.save()
                    sum.detallesuministro_set.all().delete()
                    for i in suministro['producto']:
                        det = DetalleSuministro()
                        det.suministro_id = suministro.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_details_producto(self):
        data = []
        try:
            for i in DetalleSuministro.objects.filter(suministro_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                data.append(item)
        except:
            pass
        return data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Suministro'
        context['entity'] = 'Suministro'
        context['listado_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_producto())
        return context


class SuministroDeleteView(DeleteView):
    model = Suministro
    template_name = 'suministro/delete.html'
    success_url = reverse_lazy('base:suministro_listado')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Suministro'
        context['entity'] = 'Suministro'
        context['listado_url'] = self.success_url
        return context
