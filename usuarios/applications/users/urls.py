from django.urls import path
# Views
from .views import RegistrarUsuario

app_name = 'users_app'

urlpatterns = [
    path(
        'usuario/registrar/',
        RegistrarUsuario.as_view(),
        name='add-user'
    )
]