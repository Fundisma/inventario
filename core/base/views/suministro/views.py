import json
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin

from core.base.forms import SuministroForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View

from core.base.models import Beneficiario, DetalleSuministro, Suministro, Productos
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

class SuministroListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Suministro
    template_name = 'suministro/listado.html'
    permission_required = 'view_suministro'
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
        context['title'] = 'Registro de Donaciones'
        context['create_url'] = reverse_lazy('base:suministro_create')
        context['listado_url'] = reverse_lazy('base:suministro_listado')
        context['entidad'] = 'Suministro'
        return context


class SuministroCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Suministro
    form_class = SuministroForm
    template_name = 'suministro/create.html'
    success_url = reverse_lazy('base:suministro_listado')
    permission_required = 'add_suministro'
    url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_producto':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                producto = Productos.objects.filter(stock__gt=0)
                if len(term):
                    producto = producto.filter(nombre__icontains=term)
                for i in producto.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
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
                        det.producto.stock -= det.cantidad
                        det.producto.save()
            elif action == 'search_beneficiario':
                data = []
                term = request.POST['term']
                beneficiario = Beneficiario.objects.filter(Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(documento__icontains=term))[0:10]
                for i in beneficiario:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Donacion'
        context['entidad'] = 'Servicio'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context
    
class SuministroUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Suministro
    form_class = SuministroForm
    template_name = 'suministro/create.html'
    success_url = reverse_lazy('base:suministro_listado')
    permission_required = 'change_suministro'
    url_redirect = success_url
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_producto':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                producto = Productos.objects.filter(stock__gt=0)
                if len(term):
                    producto = producto.filter(nombre__icontains=term)
                for i in producto.exclude(id__in=ids_exclude)[0:5]:
                    item = i.toJSON()
                    item['text'] = i.nombre
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
                        det.producto.stock -= det.cantidad
                        det.producto.save()
            elif action == 'edit':
                data = []
                term = request.POST['term']
                beneficiario = Beneficiario.objects.filter(Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(documento__icontains=term))[0:10]
                for i in beneficiario:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
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
        context['title'] = 'Edición de un Servicio'
        context['entidad'] = 'Servicio'
        context['listado_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_producto())
        return context


class SuministroDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Suministro
    template_name = 'suministro/delete.html'
    success_url = reverse_lazy('base:suministro_listado')
    permission_required = 'delete_suministro'
    url_redirect = success_url
    @method_decorator(csrf_exempt)
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
        context['title'] = 'Eliminación de la Donación'
        context['entidad'] = 'Servicio'
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
                'icon': '{}{}'.format(settings.MEDIA_URL, 'ho.jpg')
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
