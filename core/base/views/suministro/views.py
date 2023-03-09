import json
from django.db import transaction

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from core.base.forms import SuministroForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View

from core.base.models import DetalleSuministro, Suministro, Productos
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

class SuministroListView(ListView):
    model = Suministro
    template_name = 'suministro/listado.html'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
    @method_decorator(login_required)
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
    @method_decorator(login_required)
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
 
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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


class SuministroPdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:    
            template = get_template('suministro/factura.html')
            context = {
                'suministro': Suministro.objects.get(pk=self.kwargs['pk']),
                'comp': {'nombre': 'Biblioteca Pública Municipal de Hobo', 'dirección': 'Carrera 9° N° 5 - 41'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.jpg')
            }        
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('base:suministro_listado'))
