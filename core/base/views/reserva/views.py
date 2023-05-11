from core.base.forms import ReservaForm, ReservaUpdate
from core.base.models import Lector, Libro, Reserva
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from properties.p import Property
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin
from core.user.models import User

class ReservaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Reserva
    template_name = 'reserva/listado.html'
    permission_required = 'view_reserva'
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
                for i in Reserva.objects.all():
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
        context['title'] = 'Listado de Reservas '
        context['create_url'] = reverse_lazy('base:reserva_create')
        context['listado_url'] = reverse_lazy('base:reserva_listado')
        context['entidad'] = 'Reserva'
        return context

class ReservaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Reserva
    form_class = ReservaUpdate
    template_name = 'reserva/create.html'
    success_url = reverse_lazy('base:reserva_listado')
    permission_required = 'change_reserva'
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
            context['title'] = 'Edición de Reserva '
            context['entidad'] = 'Reserva'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class ReservaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Reserva
    template_name = 'reserva/delete.html'
    success_url = reverse_lazy('base:reserva_listado')
    permission_required = 'delete_reserva'
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
            context['title'] = 'Eliminación de Reserva '
            context['entidad'] = 'Reserva'
            context['listado_url'] = self.success_url
            return context

class ReservaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reserva/create.html'
    success_url = reverse_lazy('base:reserva_listado')
    permission_required = 'add_reserva'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        if request:
            libro = Libro.objects.filter(cantidad__gte = 1,id = request.POST.get('libro')).first()
            lector = Lector.objects.filter(id = request.POST.get('lector')).first()
            if libro and lector:
                if libro.cantidad == 0:
                    nueva_reserva = self.model(
                        estado = True,
                        libro = libro,
                        lector = lector
                    )
                    nueva_reserva.save()        
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
        context['title'] = 'Creación de Reserva '
        context['entidad'] = 'Reserva'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context
    
    
