from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from core.base.forms import AutorForm
from core.base.models import Autor
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required


class AutorView(TemplateView):
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
                for i in Autor.objects.all():
                    data.append(i.toJSON())
                
            elif action == 'add':
                aut = Autor()
                aut.nombres = request.POST['nombres']
                aut.apellidos = request.POST['apellidos']
                aut.nacionalidad = request.POST['nacionalidad']
                aut.descripcion = request.POST['descripcion']
                aut.save()
            elif action == 'edit':
                aut = Autor.objects.get(pk=request.POST['id'])
                aut.nombres = request.POST['nombres']
                aut.apellidos = request.POST['apellidos']
                aut.nacionalidad = request.POST['nacionalidad']
                aut.descripcion = request.POST['descripcion']
                aut.save()
            elif action == 'delete':
                aut = Autor.objects.get(pk=request.POST['id'])
                aut.delete()


            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de autor'
        context['list_url'] = reverse_lazy('base:autor')
        context['entity'] = 'Autor'
        context['form'] = AutorForm()
        context['entidad'] = 'Autor'
        return context

# class AutorListView(ListView):
#     model = Autor
#     template_name = 'autor/listado.html'

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'searchdata':
#                 data = []
#                 for i in Autor.objects.all():
#                     data.append(i.toJSON())
#             else: 
#                 data['error'] = 'Ha ocurrido un error'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data, safe=False)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Listado de Autores '
#         context['listado_url'] = reverse_lazy('base:autor_listado')
#         context['entidad'] = 'Autor'
#         return context


# class AutorCreateView(CreateView):
#     model = Autor
#     form_class = AutorForm
#     template_name = 'autor/create.html'
#     success_url = reverse_lazy('base:autor_listado')

    
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action'] 
#             if action == 'add':
#                 form = self.get_form()
#                 data = form.save()
            
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#      #   print(request.POST)
#       #  form = AutorForm(request.POST)
#        # if form.is_valid():
#         #    form.save()
#          #   return HttpResponseRedirect(self.success_url)
#         #self.object = None
#         #context = self.get_context_data(**kwargs)
#         #context['form'] = form
#         #return render(request, self.template_name, context)
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Creación una Autor '
#         context['entidad'] = 'Autor'
#         context['listado_url'] = reverse_lazy('base:autor_listado')
#         context['action'] = 'add'
#         return context


# class AutorUpdateView(UpdateView):
#     model = Autor
#     form_class = AutorForm
#     template_name = 'autor/create.html'
#     success_url = reverse_lazy('base:autor_listado')
    
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action'] 
#             if action == 'edit':
#                 form = self.get_form()
#                 data = form.save()
            
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             context['title'] = 'Edición una Autor '
#             context['entidad'] = 'Autor'
#             context['listado_url'] = reverse_lazy('base:autor_listado')
#             context['action'] = 'edit'
#             return context

# class AutorDeleteView(DeleteView):
#     model = Autor
#     template_name = 'autor/delete.html'
#     success_url = reverse_lazy('base:autor_listado')

#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
        
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try: 
#             self.object.delete()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)

            
#     def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             context['title'] = 'Eliminación de una autor '
#             context['entidad'] = 'Autor'
#             context['listado_url'] = reverse_lazy('base:autor_listado')
#             return context

# class AutorFormView(FormView):
#     form_class = AutorForm
#     template_name = 'autor/create.html'
#     success_url = reverse_lazy('base:autor_listado')

#     def form_valid(self, form):
#         print(form)
        
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         print(form.is_valid())
#         print(form.errors)

#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             context['title'] = 'Form │ autor '
#             context['entidad'] = 'Autor'
#             context['listado_url'] = reverse_lazy('base:autor_listado')
#             context['action'] = 'add'
#             return context