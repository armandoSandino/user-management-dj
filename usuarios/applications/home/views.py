import datetime
#
from django.shortcuts import render
#
from django.contrib.auth.mixins import LoginRequiredMixin
#
from django.urls import reverse_lazy

# Views Generic
from django.views.generic import TemplateView

# LoginRequiredMixin, indicara que necesitamos estar logueado para visualizar esta vista
class HomePage(LoginRequiredMixin, TemplateView):
    
    template_name = "home/index.html"
    # Si el usuario no esta logueado se le redigira a la siguiente ruta
    login_url = reverse_lazy('users_app:login')

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['titulo'] = 'Panel de usuario'
        context['sub_titulo'] = 'Bienvenidos'
        return context

# Un Mixon personalizado siempre debe heredar de object
class FechaMixin(object):
     
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context

class TemplatePruebaMixin(FechaMixin, TemplateView):

    template_name = 'home/mixin.html'

    
