from django.shortcuts import render
# Views Generic
from django.views.generic import TemplateView


class HomePage(TemplateView):
    
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['titulo'] = 'Panel de usuario'
        context['sub_titulo'] = 'Bienvenidos'
        return context
    
