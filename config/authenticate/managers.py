from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        """Создает и сохраняет пользователя с заданным адресом электронной почты и паролем."""

        if not email:
            raise ValueError(_('Указанный email должен быть установлен'))

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    # как сохранять простого пользователя
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_active', False)

        return self._create_user(first_name, last_name, email, password, **extra_fields)

    # как сохранять суперпользователя
    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(first_name, last_name, email, password, **extra_fields)
