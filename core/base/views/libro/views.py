
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render,redirect
from core.base.models import Libro, Reserva
from core.base.forms import LibroForm
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from core.user.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from core.base.mixins import ValidatePermissionRequiredMixin


class LibroListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Libro
    template_name = 'libro/listado.html'
    permission_required = 'view_libro'
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
                for i in Libro.objects.all():
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
        context['title'] = 'Listado de Libros '
        context['create_url'] = reverse_lazy('base:libro_create')
        context['listado_url'] = reverse_lazy('base:libro_listado')
        context['entidad'] = 'Libro'
        return context

class LibroCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/create.html'
    success_url = reverse_lazy('base:libro_listado')
    permission_required = 'add_libro'
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
        context['title'] = 'Creación de Libros '
        context['entidad'] = 'Libros'
        context['listado_url'] = self.success_url
        context['action'] = 'add'
        return context

class LibroUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/create.html'
    success_url = reverse_lazy('base:libro_listado')
    permission_required = 'change_libro'
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
            context['title'] = 'Edición de Libro '
            context['entidad'] = 'Libros'
            context['listado_url'] = self.success_url
            context['action'] = 'edit'
            return context

class LibroDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Libro
    template_name = 'libro/delete.html'
    success_url = reverse_lazy('base:libro_listado')
    permission_required = 'delete_libro'
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
            context['title'] = 'Eliminación de Libro '
            context['entidad'] = 'Libros'
            context['listado_url'] = self.success_url
            return context


class ListadoLibrosDisponibles( ListView):
    model = Libro
    paginate_by = 6
    
    template_name = 'libro/libros_disponibles.html'
    

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True,cantidad__gte = 1)
        return queryset

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Libros Disponibles '
            context['entidad'] = 'Libros Disponibles'
            return context

# def search(request):
#         queryset = request.GET.get("buscar")
#         buscar = Libro.objects.filter(estado = True, cantidad__gte = 1)
#         if queryset:
#             buscar = Libro.objects.filter(
#             Q(titulo__icontains = queryset)|
#             Q(descripcion__icontains = queryset)
#             ).distinct()

#         paginator = Paginator(buscar,6)
#         page = request.GET.get('page')
#         buscar = paginator.get_page(page) 
#         return render(request, 'libro/libros_disponibles.html',{'buscar':buscar})




class DetalleLibroDisponible(DeleteView):
    model = Libro
    template_name = 'libro/detalle_libro_disponible.html'

    def get(self,request,*args,**kwargs):
        if self.get_object().cantidad > 0:
            return render(request,self.template_name,{'object':self.get_object()})
        return redirect('base:libros_disponibles')

class RegistrarReserva(CreateView):
    model = Reserva
    success_url = reverse_lazy('base:libros_disponibles')

    def get_queryset(self):
        return self.model.objects.filter(estado = True,user  = self.request.user)

    def post(self,request,*args,**kwargs):
        data = {}
        if request:
            libro = Libro.objects.filter(id = request.POST.get('libro')).first()
            user = User.objects.filter(id = request.POST.get('user')).first()
            if libro and user:
                if libro.cantidad > 0:
                    nueva_reserva = self.model(
                        libro = libro,
                        user = user
                    )
                    nueva_reserva.save()
                    mensaje = f'{self.model.__name__} registrada correctamente!'
                    error = 'No hay error!'
                    response = JsonResponse({'mensaje': mensaje, 'error': error,'url':self.success_url})
                    response.status_code = 201
                    return response
                return redirect('base:libros_disponibles')


        