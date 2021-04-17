from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .constants import USER_TYPES, GENDER_CHOICES, ACCOUNT_TYPES, TRANSCATION_TYPE


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = None
    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, null=True, blank=True)
    account_no = models.PositiveBigIntegerField()
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email



class Transcations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default='0.00')
    Transcation_type = models.CharField(max_length=20, choices=TRANSCATION_TYPE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.Transcation_type} -> {self.user.email}'