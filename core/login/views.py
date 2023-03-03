from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from django.shortcuts import redirect
import inventario.settings as setting
from django.contrib.auth import logout

class LoginFormView(LoginView):
    template_name = 'login.html'   

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context
    

class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
