from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from django.views.generic import TemplateView
from datetime import datetime
from core.base.models import Suministro
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required


class AdminView(TemplateView):
    template_name = 'admin.html'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Suministro.objects.filter(fecha_registro__year=year, fecha_registro__month=m).aggregate(r=Coalesce(Sum('total'),0,output_field=DecimalField())).get('r')
                data.append(float(total))
        except:
            pass
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context
