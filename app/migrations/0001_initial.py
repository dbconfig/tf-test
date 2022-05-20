# Generated by Django 4.0.4 on 2022-05-20 18:59
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=64, verbose_name='ФИО кандидата')),
                ('hobbies', models.CharField(blank=True, default='', max_length=256, verbose_name='Увлечения')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
                'db_table': 'resumes',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=32, verbose_name='Навык')),
                ('resume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='skills', to='app.resume', verbose_name='Резюме')),
            ],
            options={
                'verbose_name': 'Навык',
                'verbose_name_plural': 'Навыки',
                'db_table': 'skills',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('ru', 'Русский'), ('en', 'Английский'), ('uk', 'Украинский'), ('be', 'Белорусский'), ('zn', 'Китайский')], max_length=2, verbose_name='Язык')),
                ('resume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='languages', to='app.resume', verbose_name='Резюме')),
            ],
            options={
                'verbose_name': 'Язык',
                'verbose_name_plural': 'Языки',
                'db_table': 'languages',
            },
        ),
    ]