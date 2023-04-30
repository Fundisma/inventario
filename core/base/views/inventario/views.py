from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from core.base.models import inventario
from core.base.forms import InventarioForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin


class InventarioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = inventario
    template_name = 'inventario/listado.html'
    permission_required = 'view_inventario'

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
                for i in inventario.objects.all():
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
        context['title'] = 'Listado del Inventario'
        context['create_url'] = reverse_lazy('base:inventario_create')
        context['listado_url'] = reverse_lazy('base:inventario_listado')
        context['entidad'] = 'inventario'
        return context

class InventarioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = inventario
    form_class = InventarioForm
    template_name = 'inventario/create.html'
    success_url = reverse_lazy('base:inventario_listado')
    permission_required = 'add_inventario'
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
        context['title'] = 'Creación de Inventario '
        context['entidad'] = 'inventario'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class InventarioUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = inventario
    form_class = InventarioForm
    template_name = 'inventario/create.html'
    success_url = reverse_lazy('base:inventario_listado')
    permission_required = 'change_inventario'
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
            context['title'] = 'Edición de Inventario '
            context['entidad'] = 'inventario'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class InventarioDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = inventario
    template_name = 'inventario/delete.html'
    success_url = reverse_lazy('base:inventario_listado')
    permission_required = 'delete_Inventario'
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
            context['title'] = 'Eliminación de Inventario '
            context['entidad'] = 'inventario'
            context['listado_url'] = self.success_url
            return context

