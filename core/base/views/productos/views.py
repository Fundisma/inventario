from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.base.models import Productos
from core.base.forms import ProductosForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt



class ProductosListView(ListView):
    model = Productos
    template_name = 'productos/listado.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Productos.objects.all():
                    data.append(i.toJSON())
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

class ProductosCreateView(CreateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/create.html'
    success_url = reverse_lazy('base:productos_listado')
    url_redirect = success_url
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

class ProductosUpdateView(UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/create.html'
    success_url = reverse_lazy('base:productos_listado')
    url_redirect = success_url
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

class ProductosDeleteView(DeleteView):
    model = Productos
    template_name = 'productos/delete.html'
    success_url = reverse_lazy('base:productos_listado')
    url_redirect = success_url


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

#class ProductosFormView(FormView):
 #   form_class = ProductosForm
  #  template_name = 'productos/create.html'
   # success_url = reverse_lazy('base:productos_listado')

    #def form_valid(self, form):
     #   print(form)
        
      #  return super().form_valid(form)
    
   # def form_invalid(self, form):
       # print(form.is_valid())
      #  print(form.errors)

     #   return super().form_invalid(form)

    #def get_context_data(self, **kwargs):
           # context = super().get_context_data(**kwargs)
          #  context['title'] = 'Form │ Productos'
         #   context['entidad'] = 'Productos'
        #    context['listado_url'] = reverse_lazy('base:productos_listado')
        #    context['action'] = 'add'
            #return context