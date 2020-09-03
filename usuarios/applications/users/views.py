from django.shortcuts import render
from django.urls import reverse_lazy
# Generic views
from  django.views.generic import CreateView
from django.views.generic.edit import (
    FormView
)
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
    
class RegisterUsersView(FormView):

    # Definir plantilla
    template_name = 'users/registrar_usuario.html'
    # Definir formulario personalizado a utilizar
    form_class = RegistrarUsuarioForm

    # Definir redireccion
    success_url = '.'

    def form_valid( self, form):
        # Obtner los datos del form
        usuario = form.cleaned_data['username']

        # Crear el usuario, create_user esta definida en los Managers
        User.objects.create_user(
            usuario,
            form.cleaned_data['email'],
            form.cleaned_data['contrasena'],

            nombres=form.cleaned_data['nombres'],
            apellidos =form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero']
        )
        return super(RegisterUsersView, self).form_valid(form)

