from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django_gravatar.helpers import get_gravatar_url


class AccountManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            username=kwargs.get('username')
        )

        if not kwargs.get('profile_picture'):
            if not kwargs.get('email'):
                account.profile_picture = get_gravatar_url('mgh.soufiane@gmail.com')
            else:
                account.profile_picture = get_gravatar_url(kwargs.get('email'))

        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, password, **kwargs):
        account = self.create_user(password, **kwargs)
        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(max_length=254, default='mgh.soufiane@gmail.com')
    profile_picture = models.CharField(max_length=256, blank=True, default=get_gravatar_url('mgh.soufiane@gmail.com'))
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AccountManager()

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
