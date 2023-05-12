from django.views.generic import TemplateView
from django.urls import reverse_lazy
from core.base.models import Suministro
from core.reporte.forms import ReporteForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import  csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.db.models import DecimalField


class ReporteSuministroView(TemplateView):
    template_name = 'suministro/reporte.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_reporte':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Suministro.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_registro__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.beneficiario.nombres,
                        s.beneficiario.apellidos,
                        s.beneficiario.documento,
                        s.beneficiario.telefono,
                        s.beneficiario.direccion,
                        s.beneficiario.barrio,
                        s.fecha_registro.strftime('%Y-%m-%d'),
                        format(s.total, '.3f'),
                    ])
                total = search.aggregate(r=Coalesce(Sum('total'),0,output_field=DecimalField())).get('r')
                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    '---',
                    '---',
                    '---',
                    format(total, '.3f'),
                ])
            else: 
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Servicios'
        context['entidad'] = 'Servicio'
        context['listado_url'] = reverse_lazy('suministro_reporte')
        context['form'] = ReporteForm()
        return context