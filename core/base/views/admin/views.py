from django.views.generic import TemplateView


class AdminView(TemplateView):
    template_name = 'admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        return context
