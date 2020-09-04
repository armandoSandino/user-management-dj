from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
#
from django.contrib.auth.mixins import LoginRequiredMixin

# Generic views
from  django.views.generic import CreateView, View
from django.views.generic.edit import (
    FormView
)
#Models
from .models import User
# Forms
from .forms import (
    UpdatePasswordForm,
    RegistrarUsuarioForm,
     LoginForm
) 

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

class Login(FormView):

    template_name = 'users/login.html'
    
    # Definir formulario personalizado a utilizar
    form_class = LoginForm
    # redireccion
    success_url = reverse_lazy('home_app:your-house')

    def form_valid(self, form):
        # Verificar si el usuario existe
        # El primer argumento debe ser identificado por el atributo USERNAME_FIELD del modelo User
        # Si cambias el valor de USERNAME_FIELD por el de 'email' deberias de pasar como primer argumento
        # el email a la funcion 'authenticate'
        usuario = authenticate(
            username= form.cleaned_data['nombre_de_usuario'],
            password= form.cleaned_data['contrasena']
        )
        # Aceder al sittema
        login( self.request, usuario)

        return super(Login, self).form_valid(form)

class Logout(View):
    
    #Sobreescribir 'get' del 'View'
    def get(self, request,*args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('users_app:login')
        )

#LoginRequiredMixin, indicara que solo usuarios autenticados pueden cambiar su contraseña
class UpdatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'users/actualizar_contraseña.html'
    
    # Definir formulario personalizado a utilizar
    form_class = UpdatePasswordForm
    # redireccion
    success_url = reverse_lazy('users_app:login')

    # Si el usuario no esta logueado se le redigira a la siguiente ruta
    login_url = reverse_lazy('users_app:login')

    def form_valid(self, form):
        # Antes de cambiar verificar si la contraseña del usuario activo actualmente es igual a la ingresada
        # self.request.user, nos retorna el usuario logueado, puede obtenerlo desde cualquier parte del sistema 
        
        # Verificar si el usuario existe
        # El primer argumento debe ser identificado por el atributo USERNAME_FIELD del modelo User
        # Si cambias el valor de USERNAME_FIELD por el de 'email' deberias de pasar como primer argumento
        # el email a la funcion 'authenticate'
        
        usuario_actual = self.request.user

        el_usuario = authenticate(
            username=usuario_actual.username,
            password=form.cleaned_data['contrasena_actual']
        ) 
        # Si esta logueado efectivamente puede cambiar la contraseña
        if el_usuario:
            new_pasword = form.cleaned_data['contrasena_nueva']
            usuario_actual.set_password(new_pasword)
            usuario_actual.save()

        # Cerramos la sesion    
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
