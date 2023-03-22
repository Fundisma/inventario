from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.models import Beneficiario
from core.base.forms import BeneficiarioForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt

from django.contrib.auth.decorators import login_required


class BeneficiarioListView(ListView):
    model = Beneficiario
    template_name = 'Beneficiario/listado.html'

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
                for i in Beneficiario.objects.all():
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
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('base:beneficiario_create')
        context['listado_url'] = reverse_lazy('base:beneficiario_listado')
        context['entidad'] = 'Usuarios'
        return context

class BeneficiarioCreateView(CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'beneficiario/create.html'
    success_url = reverse_lazy('base:beneficiario_listado')
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
        context['title'] = 'Creación de Usuarios'
        context['entidad'] = 'Usuarios'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class BeneficiarioUpdateView(UpdateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    template_name = 'beneficiario/create.html'
    success_url = reverse_lazy('base:beneficiario_listado')
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
            context['title'] = 'Edición de Usuarios '
            context['entidad'] = 'Usuarios'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class BeneficiarioDeleteView(DeleteView):
    model = Beneficiario
    template_name = 'beneficiario/delete.html'
    success_url = reverse_lazy('base:beneficiario_listado')
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
            context['title'] = 'Eliminación de Usuarios'
            context['entidad'] = 'Usuarios'
            context['listado_url'] = self.success_url
            return context
