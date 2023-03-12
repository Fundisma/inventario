from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.models import Autor
from core.base.forms import AutorForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt

from django.contrib.auth.decorators import login_required


class AutorListView(ListView):
    model = Autor
    template_name = 'autor/listado.html'

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
                position = 1
                for i in Autor.objects.all():
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
        context['title'] = 'Listado de Autor '
        context['create_url'] = reverse_lazy('base:autor_create')
        context['listado_url'] = reverse_lazy('base:autor_listado')
        context['entidad'] = 'Autor'
        return context

class AutorCreateView(CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'autor/create.html'
    success_url = reverse_lazy('base:autor_listado')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['title'] = 'Creación de Autor'
        context['entidad'] = 'Autor'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class AutorUpdateView(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'autor/create.html'
    success_url = reverse_lazy('base:autor_listado')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
            context['title'] = 'Edición de Autor '
            context['entidad'] = 'Autor'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class AutorDeleteView(DeleteView):
    model = Autor
    template_name = 'autor/delete.html'
    success_url = reverse_lazy('base:autor_listado')
    url_redirect = success_url

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
            context['title'] = 'Eliminación de Autor '
            context['entidad'] = 'Autor'
            context['listado_url'] = self.success_url
            return context
