from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    # Alta de usuario
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields )

    # funcion privada solo para crear un usuario
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):

        usuario = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active= is_active,
            **extra_fields
        )
        usuario.set_password(password)
        # using, permite especificar en que base de datos se creara el usuario
        usuario.save( using=self.db )
        return usuario
        
    # Alta del super usuario    
    def create_superuser(self, username, email, password=None , **extra_fields):

        return self._create_user(username, email, password, True, True, True, **extra_fields )
    
    def validar_codigo_de_verificacion(self, id_user, cod_validacion ):

        # Verificar si el codigo existe y es valido
        if self.filter( id=id_user, codregistro=cod_validacion).exists():
            return True
        else:
            return False

