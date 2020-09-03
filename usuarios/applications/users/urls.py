from django.urls import path
# Views
from .views import (
    RegistrarUsuario,
    RegisterUsersView,
    Login
) 

app_name = 'users_app'

urlpatterns = [
    path(
        'usuario/registrar/',
        RegisterUsersView.as_view(),
        name='add-user'
    ),
    path(
        'login/',
        Login.as_view(),
        name='login'
    )
]