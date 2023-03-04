from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from core.base.forms import LibroForm
from core.base.models import Libro
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required


class LibroView(TemplateView):
    model = Libro
    template_name = 'libro/listado.html'

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
                for i in Libro.objects.all():
                    data.append(i.toJSON())
                
            elif action == 'add':
                aut = Libro()
                aut.titulo = request.POST['titulo']
                aut.autor = request.POST['autor']
                aut.f_publicacion = request.POST['f_publicacion']
                aut.save()
            elif action == 'edit':
                aut = Libro.objects.get(pk=request.POST['id'])
                aut.titulo = request.POST['titulo']
                aut.autor = request.POST['autor']
                aut.f_publicacion = request.POST['f_publicacion']
                aut.save()
            elif action == 'delete':
                aut = Libro.objects.get(pk=request.POST['id'])
                aut.delete()


            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Libro'
        context['list_url'] = reverse_lazy('base:libro')
        context['entity'] = 'Libro'
        context['form'] = LibroForm()
        context['entidad'] = 'Libro'
        return context

# class LibroListView(ListView):
#     model = Libro
#     template_name = 'Libro/listado.html'

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'searchdata':
#                 data = []
#                 for i in Libro.objects.all():
#                     data.append(i.toJSON())
#             else: 
#                 data['error'] = 'Ha ocurrido un error'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data, safe=False)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Listado de Libroes '
#         context['listado_url'] = reverse_lazy('base:Libro_listado')
#         context['entidad'] = 'Libro'
#         return context


# class LibroCreateView(CreateView):
#     model = Libro
#     form_class = LibroForm
#     template_name = 'Libro/create.html'
#     success_url = reverse_lazy('base:Libro_listado')

    
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
#       #  form = LibroForm(request.POST)
#        # if form.is_valid():
#         #    form.save()
#          #   return HttpResponseRedirect(self.success_url)
#         #self.object = None
#         #context = self.get_context_data(**kwargs)
#         #context['form'] = form
#         #return render(request, self.template_name, context)
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Creación una Libro '
#         context['entidad'] = 'Libro'
#         context['listado_url'] = reverse_lazy('base:Libro_listado')
#         context['action'] = 'add'
#         return context


# class LibroUpdateView(UpdateView):
#     model = Libro
#     form_class = LibroForm
#     template_name = 'Libro/create.html'
#     success_url = reverse_lazy('base:Libro_listado')
    
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
#             context['title'] = 'Edición una Libro '
#             context['entidad'] = 'Libro'
#             context['listado_url'] = reverse_lazy('base:Libro_listado')
#             context['action'] = 'edit'
#             return context

# class LibroDeleteView(DeleteView):
#     model = Libro
#     template_name = 'Libro/delete.html'
#     success_url = reverse_lazy('base:Libro_listado')

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
#             context['title'] = 'Eliminación de una Libro '
#             context['entidad'] = 'Libro'
#             context['listado_url'] = reverse_lazy('base:Libro_listado')
#             return context

# class LibroFormView(FormView):
#     form_class = LibroForm
#     template_name = 'Libro/create.html'
#     success_url = reverse_lazy('base:Libro_listado')

#     def form_valid(self, form):
#         print(form)
        
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         print(form.is_valid())
#         print(form.errors)

#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             context['title'] = 'Form │ Libro '
#             context['entidad'] = 'Libro'
#             context['listado_url'] = reverse_lazy('base:Libro_listado')
#             context['action'] = 'add'
#             return context