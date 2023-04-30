from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.models import categoriaLibro
from core.base.forms import CategoriaLibroForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin

from django.contrib.auth.decorators import login_required


class CategoriaLibroListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = categoriaLibro
    template_name = 'categoriaLibro/listado.html'
    permission_required = 'view_categoriaLibro'
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
                for i in categoriaLibro.objects.all():
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
        context['title'] = 'Listado de Categorías '
        context['create_url'] = reverse_lazy('base:categoriaLibro_create')
        context['listado_url'] = reverse_lazy('base:categoriaLibro_listado')
        context['entidad'] = 'Categorías'
        return context

class CategoriaLibroCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = categoriaLibro
    form_class = CategoriaLibroForm
    template_name = 'categoriaLibro/create.html'
    success_url = reverse_lazy('base:categoriaLibro_listado')
    permission_required = 'add_categoriaLibro'
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
        context['title'] = 'Creación de Categorías'
        context['entidad'] = 'Categorías'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class CategoriaLibroUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = categoriaLibro
    form_class = CategoriaLibroForm
    template_name = 'categoriaLibro/create.html'
    success_url = reverse_lazy('base:categoriaLibro_listado')
    permission_required = 'change_categoriaLibro'
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
            context['title'] = 'Edición de Categorías '
            context['entidad'] = 'Categorías'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class CategoriaLibroDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = categoriaLibro
    template_name = 'categoriaLibro/delete.html'
    success_url = reverse_lazy('base:categoriaLibro_listado')
    permission_required = 'delete_categoriaLibro'
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
            context['title'] = 'Eliminación de Categorías '
            context['entidad'] = 'Categorías'
            context['listado_url'] = self.success_url
            return context
