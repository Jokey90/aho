from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class ADUserManager(BaseUserManager):
    def create_user(self, login):
        if not login:
            raise ValueError('У пользователя обязательно должен быть логин')

        user = self.model(
            login=login
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, login):
        user = self.create_user(login)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class ADUser(AbstractBaseUser):
    login = models.CharField(verbose_name='Логин', unique=True, max_length=50)
    full_name = models.CharField(verbose_name='Имя', max_length=100)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    is_admin = models.BooleanField(verbose_name='Администратор', default=False)
    is_staff = models.BooleanField(verbose_name='Доступ к админке', default=False)

    objects = ADUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['login']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.login

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def staff(self):
        return self.is_staff or self.is_admin