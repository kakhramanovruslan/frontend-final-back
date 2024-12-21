from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, verbose_name=_('Email'), max_length=150, unique=True)
    first_name = models.CharField(db_index=True, verbose_name=_('Имя'), max_length=150)
    last_name = models.CharField(db_index=True, verbose_name=_('Фамилия'), max_length=150)
    phone = models.CharField(db_index=True, verbose_name=_('Номер телефона'), unique=True, max_length=15)

    iin = models.CharField(max_length=12, verbose_name=_('ИИН'), unique=True, null=True, blank=True)
    id_card_image = models.FileField(
        upload_to='uploads/id_cards/', verbose_name=_('Изображение удостоверения личности'), null=True, blank=True)

    is_staff = models.BooleanField(default=False, verbose_name=_('Персонал'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'iin', 'id_card_image']

    objects = UserManager()

    class Meta:
        ordering = ['id']
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class UserPaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    card_number = models.CharField(max_length=16, verbose_name=_('Номер карты'))
    card_holder_name = models.CharField(max_length=150, verbose_name=_('Имя держателя карты'))
    expiration_date = models.DateField(verbose_name=_('Срок действия'))
    cvv = models.CharField(max_length=3, verbose_name=_('CVV код'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Обновлено'))

    class Meta:
        ordering = ['id']
        verbose_name = _('Платежная карта')
        verbose_name_plural = _('Платежные карты')

    def __str__(self):
        return self.card_number