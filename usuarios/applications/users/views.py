from django.shortcuts import render
from django.urls import reverse_lazy
# Generic views
from  django.views.generic import CreateView
#Models
from .models import User
# Forms
from .forms import RegistrarUsuarioForm

class RegistrarUsuario(CreateView):

    template_name = 'users/registrar_usuario.html'
    # Definir formulario personalizado a utilizar
    form_class = RegistrarUsuarioForm
    
    # Definir redireccion
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(RegistrarUsuario, self).get_context_data(**kwargs)
        context['titulo'] = 'Registrar usuario'
        return context
    


