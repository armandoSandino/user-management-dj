from django import forms
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

