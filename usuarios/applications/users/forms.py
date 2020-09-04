from django import forms
# Funcion para autenticar
from django.contrib.auth import authenticate
# Models
from .models import User

class RegistrarUsuarioForm(forms.ModelForm):

    # Definir campos del form que no son miembros de nuestro modelo
    contrasena = forms.CharField(
        label='Contraseña',
        required= True,
        widget= forms.PasswordInput(
            attrs= {
                'placeholder': 'Su contraseña'
            }
        )
    )
    repetir_contrasena = forms.CharField(
        label='Repetir Contraseña',
        required= True,
        widget= forms.PasswordInput(
            attrs= {
                'placeholder': 'Repita la contraseña'
            }
        )
    )

    class Meta:
        # Definir modelo a implementar
        model = User
        # Campos a utlizar, __all__ indicara todos los campos
        #fields = ('__all__')
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero'
        )

    # Validar contraseña, utiliza 'clean_' seguida del campo  a validar
    def clean_repetir_contrasena(self):

        if self.cleaned_data['contrasena'] != self.cleaned_data['repetir_contrasena']:
            # Mostrar mensaje informativo
            # add_error(campo, mensaje), muestra un mensaje en el campo especificado en su primer parametro
            self.add_error('repetir_contrasena', 'Las contraseñas no son iguales..')

 # Heredamos de 'forms.Form' y no de 'forms.ModelForm' por que no estamos dependiendo de ningun modelo en especifico    
class LoginForm(forms.Form):

    nombre_de_usuario = forms.CharField(
        label='Nombre de usuario',
        required= True,
        widget= forms.TextInput(
            attrs= {
                'placeholder': 'Ingrese el usuario',
                'style': '{margin: 10px }'
            }
        )
    )
    
    contrasena = forms.CharField(
        label='Contraseña',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder': 'Ingrese la contraseña',
                'style': '{padding: 1em}'
            }
        )
    )

    # sino le especificas sobre que campo quieres validar puedes simplemente indicar 'clean'
    # Django ejecutara esta validacion antes de todas las demas que tengas definidas
    def clean(self):
        
        cleaned_data = super(LoginForm, self).clean()

        #Obtener datos
        usuario = self.cleaned_data['nombre_de_usuario']
        contrasena = self.cleaned_data['contrasena']

        # El primer argumento debe ser identificado por el atributo USERNAME_FIELD del modelo User
        # Si cambias el valor de USERNAME_FIELD por el de 'email' deberias de pasar como primer argumento
        # el email a la funcion 'authenticate'

        # Veriricar si esta autenticado
        if not authenticate( username =usuario,password= contrasena):
            raise forms.ValidationError('Las credenciales no son correctas')

        return self.cleaned_data

# Heredamos de 'forms.Form' y no de 'forms.ModelForm' por que no estamos dependiendo de ningun modelo en especifico
class UpdatePasswordForm(forms.Form):
        
    contrasena_actual = forms.CharField(
        label='Contraseña actual',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder': 'Ingrese la contraseña actual',
                'style': '{padding: 1em}'
            }
        )
    )      
    contrasena_nueva = forms.CharField(
        label='Contraseña nueva',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder': 'Ingrese la contraseña nueva',
                'style': '{padding: 1em}'
            }
        )
    )

# Heredamos de 'forms.Form' y no de 'forms.ModelForm' por que no estamos dependiendo de ningun modelo en especifico


class VerifiricacionForm(forms.Form):

    codigo_registro = forms.CharField(required=True)

    # THE_ID, viaja desde el FormView que implementa este Form
    def __init__(self, THE_ID,  *args, **kwargs):
        self.ID_USUARIO = THE_ID 
        super(VerifiricacionForm, self).__init__(*args,**kwargs)

    # Validar codigo, utiliza 'clean_' seguida del campo  a validar
    def clean_codigo_registro(self):

        codigo = self.cleaned_data['codigo_registro']

        if  len(codigo) == 6:
            
            # Verificamos si el codigo y el id del usuario es valido
            
            activo = User.objects.validar_codigo_de_verificacion(
                self.ID_USUARIO,
                codigo
            )
            if not activo:
                raise  forms.ValidationError('Error, el codigo de verificacion es incorrecto..')
        else:
            # add_error(campo, mensaje), muestra un mensaje en el campo especificado en su primer parametro
            # self.add_error('codigo_registro')
            raise forms.ValidationError('El codigo de verificacion es incorrecto..')
