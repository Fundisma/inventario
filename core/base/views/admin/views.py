from django.db.models import Sum
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from datetime import datetime
from core.base.models import Suministro
from core.base.models import *

class AdminView(TemplateView):
    template_name = 'admin.html'

    def get_grafico(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Suministro.objects.filter(fecha_registro__year=year,fecha_registro__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                data.append(float(total))
        except:
            pass
        return data
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['grafico'] = self.get_grafico()
        return context
