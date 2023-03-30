from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.base.models import Productos
from core.base.forms import ProductosForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin


class ProductosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Productos
    template_name = 'productos/listado.html'
    permission_required = 'view_productos'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Productos.objects.all():
                    item = i.toJSON()
                    item['position']  = position
                    data.append(item)
                    position += 1 
            else: 
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Producto '
        context['create_url'] = reverse_lazy('base:productos_create')
        context['listado_url'] = reverse_lazy('base:productos_listado')
        context['entidad'] = 'Productos'
        return context

class ProductosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/create.html'
    success_url = reverse_lazy('base:productos_listado')
    permission_required = 'add_productos'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action'] 
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Productos '
        context['entidad'] = 'Productos'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class ProductosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/create.html'
    success_url = reverse_lazy('base:productos_listado')
    permission_required = 'change_productos'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action'] 
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Edición de Productos '
            context['entidad'] = 'Productos'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class ProductosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Productos
    template_name = 'productos/delete.html'
    success_url = reverse_lazy('base:productos_listado')
    permission_required = 'delete_productos'
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
            context['title'] = 'Eliminación de Productos '
            context['entidad'] = 'Productos'
            context['listado_url'] = self.success_url
            return context

