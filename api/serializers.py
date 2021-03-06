from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import Resume
from app.types import LanguageChoices

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class ResumeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128, allow_blank=True)
    hobbies = serializers.CharField(max_length=256, allow_blank=True)
    skills = serializers.ListField(child=serializers.CharField(), default=list())
    languages = serializers.ListField(child=serializers.CharField(), default=list())
    class Meta:
        model = Resume
        fields = ('id', 'name', 'hobbies', 'skills', 'languages')
    def validate(self, data):
        splitted_full_name = data['name'].split()
        # Проверяем, чтобы в ФИО было минимум 2 слова, а также чтобы в каждом слове было минимум 2 символа
        if len(splitted_full_name) < 2 or not all(map(lambda word: len(word) >= 2, splitted_full_name)):
            raise serializers.ValidationError('Введёно некорректное ФИО')
        elif len(data['hobbies']) == 0:
            raise serializers.ValidationError('Пожалуйста, заполните поле "Интересы"')
        elif len(data['languages']) == 0:
            raise serializers.ValidationError('Пожалуйста, укажите хотя бы один язык')
        elif len(data['skills']) == 0:
            raise serializers.ValidationError('Пожалуйста, укажите хотя бы один навык')
        return data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16, allow_blank=True)
    password = serializers.CharField(max_length=32, allow_blank=True)
    password_again = serializers.CharField(max_length=32, allow_blank=True)
    def validate(self, data):
        if data['username'] == '' or data['password'] == '':
            raise serializers.ValidationError('Необходимо указать имя пользователя и пароль')
        if not data['password'] == data['password_again']:
            raise serializers.ValidationError('Пароли не совпадают!')
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16, allow_blank=True)
    password = serializers.CharField(max_length=32, allow_blank=True)
    def validate(self, data):
        if data['username'] == '' or data['password'] == '':
            raise serializers.ValidationError('Необходимо указать имя пользователя и пароль')
        return data
