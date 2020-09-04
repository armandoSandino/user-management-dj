from django.shortcuts import render
# For send email
from django.core.mail import send_mail
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
    LoginForm,
    VerifiricacionForm
) 
# Functions
from .functions import generar_codigo

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
        
        # Generamos el cofigo para verificacion de la cuenta via email
        codigo = generar_codigo()

        # Crear el usuario, create_user esta definida en los Managers
        # datos_del_usuario, almacena la data del usuario luego de su creacion
        datos_del_usuario = User.objects.create_user(
            usuario,
            form.cleaned_data['email'],
            form.cleaned_data['contrasena'],

            nombres=form.cleaned_data['nombres'],
            apellidos =form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo
        )
        # Enviar el codigo al correo del usuario
        asunto = 'Confirmacion de correo'
        mensaje= 'Codigo de verifricacion '+ codigo
        email_remitente = 'jonwinlive@gmail.com'
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'], ] )

        #return super(RegisterUsersView, self).form_valid(form)
        # En el segundo parametro del 'reverse' especificamos los parametros a pasarle a la ruta
        return HttpResponseRedirect(
            reverse(
                'users_app:verification-account',
                kwargs={'pk': datos_del_usuario.id }
            )
        )

class CodeVerificationView(FormView):
    ''' Vista para la verificacion de cuenta '''
    template_name = 'users/verification.html'
    # Definir formulario
    form_class = VerifiricacionForm
    # Ruta de redireccion
    success_url = reverse_lazy('users_app:login')

    # Para que en el Form  pueda acceder al 'kwargs' y obtener los valores del url
    # debes mandarlo desde el FormView sobre escribiendo el get_form_kwargs
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        # Enviamos el parametro de la url al Form
        kwargs.update({
            'THE_ID': self.kwargs['pk']
        })
        return kwargs

    def form_valid( self, form):
        #
        # Si todo esta bien actualizaremos el campor is_active del registro
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )
        return super(CodeVerificationView, self).form_valid(form)
        '''
        codigo = form.cleaned_data['codigo_registro']

        if len(codigo) == 6:
            # Verificamos si el codigo y el id del usuario es valido
            activo = User.objects.validar_codigo_de_verificacion(
                id_user,
                codigo
            )
            if not activo:
                form.add_error('codigo_registro', 'Las contraseñas no son iguales..')
                # raise forms.ValidationError("Document already exists in DB")
                return HttpResponseRedirect(
                    reverse(
                        'users_app:verification-account',
                        kwargs={'pk': id_user }
                    )
                )
            else:
                return super(CodeVerificationView, self).form_valid(form)
        else:
            return HttpResponseRedirect(
                reverse(
                    'users_app:verification-account',
                    kwargs={'pk': id_user }
                )
            )
            '''

        

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
