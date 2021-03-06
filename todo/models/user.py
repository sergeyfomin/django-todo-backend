from django.db import models
 
import re

from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser,
                     **extra_fields):
        now = timezone.now()

        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)

        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Username',
        max_length=30,
        unique=True,
        help_text='Required. 30 characters or fewer. Letters, '
                  'numbers and @/./+/-/_ characters',
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Enter a valid username.',
                'invalid'
            )
        ]
    )
    first_name = models.CharField(
        'Имя',
        max_length=30,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=30,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Email',
        max_length=255
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_active = models.BooleanField(
        'active',
        default=False,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.'
    )
    date_joined = models.DateTimeField(
        'date joined',
        default=timezone.now
    )
    receive_newsletter = models.BooleanField(
        'receive newsletter',
        default=False
    )

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,

        }

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    objects = UserManager()
