from django.views.generic import TemplateView, ListView, DeleteView
from django.shortcuts import render, redirect
from core.base.models import Eventos, Libro

class IndexView(TemplateView):
    
    template_name = 'index.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True)
        return queryset
    
class BibliotecaView(ListView):

    model = Libro
    paginate_by = 9
    template_name = 'biblioteca.html'
    
    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True,cantidad__gte = 1)
        return queryset
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

class DetalleLibro(DeleteView):
    model = Libro
    template_name = 'librosDetalle.html'

    def get(self,request,*args,**kwargs):
        if self.get_object().cantidad > 0:
            return render(request,self.template_name,{'object':self.get_object()})
        return redirect('principal:biblioteca')
    
class EventosView(ListView):

    model = Eventos
    paginate_by = 3
    template_name = 'eventos.html'
    
    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True)
        return queryset
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

