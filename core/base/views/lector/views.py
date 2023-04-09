from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.models import Lector
from core.base.forms import LectorForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin

from django.contrib.auth.decorators import login_required 


class LectorListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Lector
    template_name = 'lector/listado.html'
    permission_required = 'view_lector'
    
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
                for i in Lector.objects.all():
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
        context['title'] = 'Listado de Lectores'
        context['create_url'] = reverse_lazy('base:lector_create')
        context['listado_url'] = reverse_lazy('base:lector_listado')
        context['entidad'] = 'Lector'
        return context

class LectorCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Lector
    form_class = LectorForm
    template_name = 'lector/create.html'
    success_url = reverse_lazy('base:lector_listado')
    permission_required = 'add_Lector'
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
        context['title'] = 'Creación de Lectores'
        context['entidad'] = 'Lector'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class LectorUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Lector
    form_class = LectorForm
    template_name = 'lector/create.html'
    success_url = reverse_lazy('base:lector_listado')
    permission_required = 'change_lector'
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
            context['title'] = 'Edición de Lectores '
            context['entidad'] = 'Lector'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class LectorDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Lector
    template_name = 'lector/delete.html'
    success_url = reverse_lazy('base:lector_listado')
    permission_required = 'delete_lector'
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
            context['title'] = 'Eliminación de Lector'
            context['entidad'] = 'Lector'
            context['listado_url'] = self.success_url
            return context
