from django.contrib import admin
from app.models import *


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'name', 'hobbies')
    list_display = ('user', 'name', 'hobbies')
    search_fields = ('name', 'hobbies')
    readonly_fields = ('id',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    fields = ('id', 'resume', 'value')
    list_display = ('resume', 'value',)
    search_fields = ('value',)
    readonly_fields = ('id',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fields = ('id', 'resume', 'language')
    list_display = ('resume', 'language',)
    list_filter = ('language',)
    readonly_fields = ('id',)
