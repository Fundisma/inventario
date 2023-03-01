from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.base.models import Categoria
from core.base.forms import CategoriaForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt



class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/listado.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else: 
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorías '
        context['create_url'] = reverse_lazy('base:categoria_create')
        context['listado_url'] = reverse_lazy('base:categoria_listado')
        context['entidad'] = 'Categorias'
        return context

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/create.html'
    success_url = reverse_lazy('base:categoria_listado')

    
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
     #   print(request.POST)
      #  form = CategoriaForm(request.POST)
       # if form.is_valid():
        #    form.save()
         #   return HttpResponseRedirect(self.success_url)
        #self.object = None
        #context = self.get_context_data(**kwargs)
        #context['form'] = form
        #return render(request, self.template_name, context)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Categoria '
        context['entidad'] = 'Categorias'
        context['listado_url'] = reverse_lazy('base:categoria_listado')
        context['action'] = 'add'
        return context

class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria/create.html'
    success_url = reverse_lazy('base:categoria_listado')
    
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
            context['title'] = 'Edición una Categoria '
            context['entidad'] = 'Categorias'
            context['listado_url'] = reverse_lazy('base:categoria_listado')
            context['action'] = 'edit'
            return context

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'categoria/delete.html'
    success_url = reverse_lazy('base:categoria_listado')

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
            context['title'] = 'Eliminación de una Categoria '
            context['entidad'] = 'Categorias'
            context['listado_url'] = reverse_lazy('base:categoria_listado')
            return context

class CategoriaFormView(FormView):
    form_class = CategoriaForm
    template_name = 'categoria/create.html'
    success_url = reverse_lazy('base:categoria_listado')

    def form_valid(self, form):
        print(form)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.is_valid())
        print(form.errors)

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Form │ Categoria '
            context['entidad'] = 'Categorias'
            context['listado_url'] = reverse_lazy('base:categoria_listado')
            context['action'] = 'add'
            return context