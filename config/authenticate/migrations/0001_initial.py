# Generated by Django 5.1.4 on 2024-12-19 12:19

import authenticate.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=150, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(db_index=True, max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(db_index=True, max_length=150, verbose_name='Фамилия')),
                ('phone', models.CharField(db_index=True, max_length=15, unique=True, verbose_name='Номер телефона')),
                ('iin', models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='ИИН')),
                ('id_card_image', models.FileField(blank=True, null=True, upload_to='uploads/id_cards/', verbose_name='Изображение удостоверения личности')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'объект "Пользователь"',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['id'],
            },
            managers=[
                ('objects', authenticate.managers.UserManager()),
            ],
        ),
    ]
