from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# PermissionsMixin, no permitira que gestionemos tanto usuarios administradores o regulares

class User(AbstractBaseUser, PermissionsMixin):

    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros')
    )
    username = models.CharField('User name', max_length=10, unique=True, blank= False)
    email = models.EmailField(blank=False)
    nombres = models.CharField('Nombres', max_length=30, blank=False)
    apellidos = models.CharField('Apellidos', max_length=30, blank=False)
    genero = models.CharField('Genero', max_length=1, choices= GENERO_CHOICES,  blank=True) 
    
    # Especificar cual sera el nombre de usuario con el cual se utenticara el super usuario de Django
    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos
