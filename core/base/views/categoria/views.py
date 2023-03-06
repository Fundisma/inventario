from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.base.forms import CategoriaForm
from core.base.models import Categoria

from django.contrib.auth.decorators import login_required

class CategoriaView(TemplateView):
    model = Categoria
    template_name = 'categoria/listado.html'

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
                for i in Categoria.objects.all():
                    item = i.toJSON()
                    item['position']  = position
                    data.append(item)
                    position += 1 
                
            elif action == 'add':
                ben = Categoria()
                ben.nombre = request.POST['nombre']
                ben.descripcion = request.POST['descripcion']
                ben.save()
            elif action == 'edit':
                ben = Categoria.objects.get(pk=request.POST['id'])
                ben.nombre = request.POST['nombre']
                ben.descripcion = request.POST['descripcion']
                ben.save()
            elif action == 'delete':
                ben = Categoria.objects.get(pk=request.POST['id'])
                ben.delete()


            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categoria'
        context['list_url'] = reverse_lazy('base:categoria')
        context['entity'] = 'Categoria'
        context['form'] = CategoriaForm()
        context['entidad'] = 'Categoria'
        return context
