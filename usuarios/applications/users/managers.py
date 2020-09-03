from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    # def create_user(self):

    # funcion privada solo para crear un super administrador
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):

        usuario = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        usuario.set_password(password)
        # using, permite especificar en que base de datos se creara el usuario
        usuario.save( using=self.db )
        return usuario
        
    # Alta del super usuario    
    def create_superuser(self, username, email, password=None , **extra_fields):

        return self._create_user(username, email, password, True, True, **extra_fields )
