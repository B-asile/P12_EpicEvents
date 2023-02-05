from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group


class UserManager(BaseUserManager):
    """User profiles Manager : create & save"""
    def create_user(self, email, first_name, last_name, password=None, group=None):
        """Create new user profile"""
        if not email:
            raise ValueError('adresse email requise ou invalide')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            group=group
        )
        user.set_password(password)
        user.save(using=self._db)
        # force add user in group if not admin (because admin don't got group)
        if group:
            group.user_set.add(user)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Create new admin profile"""
        user = self.create_user(
            email,
            first_name,
            last_name,
            password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model for user data in the system"""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        default=None,
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email