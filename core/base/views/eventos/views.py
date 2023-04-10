from core.base.forms import EventosForm
from core.base.models import Eventos
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin


class EventosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Eventos
    template_name = 'eventos/listado.html'
    permission_required = 'view_eventos'
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
                for i in Eventos.objects.all():
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
        context['title'] = 'Listado de Eventos '
        context['create_url'] = reverse_lazy('base:eventos_create')
        context['listado_url'] = reverse_lazy('base:eventos_listado')
        context['entidad'] = 'Eventos'
        return context

class CalendarView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Eventos
    template_name = 'eventos/calendar.html'
    permission_required = 'view_eventos'
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
                for i in Eventos.objects.all():
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
        context['title'] = 'Eventos '
        context['entidad'] = 'Eventos'
        return context
    

class EventosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Eventos
    form_class = EventosForm
    template_name = 'eventos/create.html'
    success_url = reverse_lazy('base:eventos_listado')
    permission_required = 'add_eventos'
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
        context['title'] = 'Creación de Eventos '
        context['entidad'] = 'Eventos'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class EventosUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Eventos
    form_class = EventosForm
    template_name = 'eventos/create.html'
    success_url = reverse_lazy('base:eventos_listado')
    permission_required = 'change_eventos'
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
            context['title'] = 'Edición de Eventos '
            context['entidad'] = 'Eventos'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class EventosDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Eventos
    template_name = 'eventos/delete.html'
    success_url = reverse_lazy('base:eventos_listado')
    permission_required = 'delete_eventos'
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
            context['title'] = 'Eliminación de Eventos '
            context['entidad'] = 'Eventos'
            context['listado_url'] = self.success_url
            return context
