from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.types import LanguageChoices


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    # Создаём резюме сразу после создания нового объекта
    if created:
        Resume(user=instance).save()


class Resume(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='resume', verbose_name='Пользователь',
                                null=True)
    name = models.CharField(max_length=64, verbose_name='ФИО кандидата', blank=True, default='')
    hobbies = models.CharField(max_length=256, verbose_name='Увлечения', blank=True, default='')

    class Meta:
        db_table = 'resumes'
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'

    def __str__(self):
        return self.name


class Skill(models.Model):
    resume = models.ForeignKey(to=Resume, on_delete=models.SET_NULL, related_name='skills', verbose_name='Резюме',
                               null=True)
    value = models.CharField(max_length=32, verbose_name='Навык')

    class Meta:
        db_table = 'skills'
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.value


class Language(models.Model):
    resume = models.ForeignKey(to=Resume, on_delete=models.SET_NULL, related_name='languages', verbose_name='Резюме',
                               null=True)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices, verbose_name='Язык')

    class Meta:
        db_table = 'languages'
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'
