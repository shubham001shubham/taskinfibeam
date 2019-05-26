
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email,password,is_staff, is_superuser,**extra_fields):
        now = timezone.now()


        if not email:
            raise ValueError('users must have an email address')
        email = self.normalize_email(email)
        #location  = location
        user = self.model(email = email,
                            is_staff = is_staff,
                            is_superuser = is_superuser,
                            last_login = now,
                            date_joined = now, #location = location,
                            **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_user(self, email, password=None,**extra_fields):
        user = self._create_user(email, password, location, False, False, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """My own custom user class"""

    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name=_('email address'))
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    location = models.CharField(max_length=200,default='')
    #location = models.CharField()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the email."""
        return self.email

    def get_short_name(self):
        """Return the email."""
        return self.email


from .models import User as LUser
class ImageUpload(models.Model):
    title = models.CharField(max_length=255)
    url = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to='image/')
    body = models.TextField()
    email = models.ForeignKey(LUser, on_delete=models.CASCADE)
    comment = models.TextField(default="")

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
