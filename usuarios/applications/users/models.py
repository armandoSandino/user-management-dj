from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Managers
from .managers import UserManager

# PermissionsMixin, no permitira que gestionemos tanto usuarios administradores o regulares
class User(AbstractBaseUser, PermissionsMixin):

    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros')
    )
    username = models.CharField('User name', max_length=10, unique=True, blank= False)
    email = models.EmailField(blank=False)
    nombres = models.CharField('Nombres', max_length=30, blank=True)
    apellidos = models.CharField('Apellidos', max_length=30, blank=True)
    genero = models.CharField('Genero', max_length=1, choices= GENERO_CHOICES,  blank=True) 
    # Codigo de verificacion
    codregistro = models.CharField(max_length=6, default=True)

    is_staff = models.BooleanField(default=False)
    # Para al verificacion de una cuenta activa
    is_active = models.BooleanField(default=False)

    
    # Especificar cual sera el nombre de usuario con el cual se utenticara el super usuario de Django
    USERNAME_FIELD = 'username'

    # Especificar los campos para la autenticacion del administrador
    REQUIRED_FIELDS = ['email',]

    # Especificar el Manager a utilizar
    objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos
