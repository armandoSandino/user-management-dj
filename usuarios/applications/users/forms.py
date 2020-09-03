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
