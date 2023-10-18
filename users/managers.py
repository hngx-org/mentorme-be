from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Manager of the user email"""
    
    def create_user(self, email, password=None, **extra_fields):
        """create_user returns a user 
        
        args: (email)
              (password)
        returns: a new user

        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
    def create_superuser(self, email, password=None, **extra_fields):
        """create_user returns a user 
        
        args: (email)
              (password)
        returns: a new superuser

        """
        
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("verified", True)

        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
