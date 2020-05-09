import uuid
import os
from datetime import timedelta
from datetime import datetime

from django.conf import settings
from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from django.utils.timezone import now

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise AttributeError('Users must have an email address')
        if not first_name:
            raise AttributeError('Users must have a first_name')
        if not last_name:
            raise AttributeError('Users must have an last_name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.activation_date = now()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    first_name = models.CharField(
        max_length=60
    )
    last_name = models.CharField(
        max_length=60
    )
    is_active = models.BooleanField(
        default=False
    )
    is_admin = models.BooleanField(
        default=False
    )
    registration_date = models.DateTimeField(
        auto_now_add=True
    )
    activation_key = models.CharField(
        max_length=8,
        blank=True
    )
    activation_key_creation_time = models.DateTimeField(
        blank=True,
        null=True
    )
    activation_date = models.DateTimeField(
        blank=True,
        null=True,
        editable=False
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.is_active and self.activation_key == '':
            self.activation_key = self.create_activation_key()
            self.activation_key_creation_time = now()
        if self.is_active and self.activation_key != '':
            self.activation_key = ''
            self.activation_date = now()
        super().save(*args, **kwargs)

    def create_activation_key(self):
        key = uuid.uuid4().hex[:8]
        while User.objects.filter(activation_key=key).exists():
            key = uuid.uuid4().hex[:8]
        return key

    @property
    def full_name(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def activation_key_is_valid(self):
        return (
            self.activation_key_creation_time < (
                now() + timedelta(
                    minutes=int(
                        settings.ENV['ACTIVATION_KEY_PERIOS_OF_VALIDITY']
                    )
                )
            )
        )

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_activation_message(self):
        mail_template_path = os.path.join(
            settings.BASE_DIR,
            'User',
            'User',
            'templates',
            'mails',
            'activation.html'
        )

        mail_template = open(mail_template_path, 'r')
        body = mail_template.read()
        mail_template.close()
        activation_link = "{}{}?key={}".format(
            settings.ENV['FRONTEND_URL'],
            settings.ENV['FRONTEND_ACCOUNT_ACTIVATION_URL'],
            self.activation_key
        )
        body = body.replace('{{USER}}', self.first_name)
        body = body.replace('{{ACTIVATION_KEY}}', activation_link)
        return body
