from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from prastuti.settings import EMAIL_HOST_USER

class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a CustomUser with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular CustomUser with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('name', 'admin')
        extra_fields.setdefault('institute', 'IIT BHU')
        extra_fields.setdefault('year', 3)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email adress'), unique=True)
    USERNAME_FIELD = 'email'
    name = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('users:userprofile', kwargs={'email': self.email})
    
    def email_user(self, subject, message, from_email):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email])



# added signals
