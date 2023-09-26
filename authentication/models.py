from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    
    def create_user(self,username,email,password=None):
        if username is None :
            raise TypeError('you should have a username')
        if email is None :
            raise TypeError('you should have a email')
        
        
        user = self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified=True
        user.save()
        return user
        






class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.SmallIntegerField(blank=True,null=True)
    birthdate = models.DateField(blank=True,null=True)
    major = models.CharField(max_length=100, blank=True,null=True)
    no_of_reports = models.IntegerField(default=0)
    profile_pic = models.ImageField(blank=True,null=True,upload_to='profile/')
    
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    objects = UserManager()
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance :
        if instance.no_of_reports >=50 :
            instance.is_active =False