from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyAccountManager(BaseUserManager):
    """
        Custom account manager (administrator, superuser, user, etc.)
    """

    def create_user(self, first_name, last_name, username, email, password=None):
        """
            Custom create user function.
                - first_name  : str
                - last_name   : str
                - username    : str
                - email       : str
                - password    : str (default=None)
        """
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """
            Custom create superuser function.

                - first_name  : str
                - last_name   : str
                - username    : str
                - email       : str
                - password    : str
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)

        profile = UserProfile()
        profile.user_id = user.id
        profile.profile_picture = 'default/default-user.png'
        profile.save()

        return user


class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=64)
    last_name       = models.CharField(max_length=64)
    username        = models.CharField(max_length=64, unique=True)
    email           = models.EmailField(max_length=128, unique=True)
    phone_number    = models.CharField(max_length=64)

    # Required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    # email is the element used for the authentication
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class UserProfile(models.Model):
    user                = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture     = models.ImageField(upload_to='userprofile', blank=True)
    address_line_1      = models.CharField(max_length=128, blank=True)
    address_line_2      = models.CharField(max_length=128, blank=True)
    country             = models.CharField(max_length=64)
    state               = models.CharField(max_length=64)
    city                = models.CharField(max_length=64)

    def __str__(self):
        return self.user.full_name()

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
