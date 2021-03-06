from traceback import print_exc
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import *
from app.services import UserService, ResumeService


def get_response(action: str, success: bool, message=None, data=None):
    return {
        'action': action,
        'success': success,
        'message': message,
        'data': data
    }


def handle_errors(action: str) -> callable:
    def decorator(func: callable) -> callable:
        def wrapper(*args, **kwargs):
            # Ловим ВСЕ ошибки
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print_exc()
                response = get_response(action, False, str(e))
                return Response(status=500, data=response)

        return wrapper

    return decorator


class RegisterView(APIView):
    """APIView для регистрации пользователя"""
    permission_classes = (AllowAny,)
    action = 'register'

    @handle_errors(action)
    def post(self, request, *args, **kwargs):
        # Проверяем полученные данные
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(status=400, data=get_response(self.action, False, serializer.errors['non_field_errors'][0]))
        # Получаем имя пользователя и пароль
        username = serializer.data['username']
        password = serializer.data['password']
        # Проверяем, нет ли пользователя с таким именем пользователя
        if UserService.is_username_exists(username):
            response = get_response(self.action, False, 'Пожалуйста, выберите другое имя пользователя')
            return Response(status=409, data=response)
        # Создаём пользователя
        user = UserService.create_user(username, password)
        # Авторизуем пользователя
        login(request, user)
        # Возвращаем 201 Created
        response = get_response(self.action, True, None)
        return Response(status=201, data=response)


class LoginView(APIView):
    """APIView для входа пользователя в систему"""
    permission_classes = (AllowAny,)
    action = 'login'

    @handle_errors(action)
    def post(self, request, *args, **kwargs):
        # Проверяем полученные данные
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(status=400, data=get_response(self.action, False, serializer.errors['non_field_errors'][0]))

        # Получаем имя пользователя и пароль
        username = serializer.data['username']
        password = serializer.data['password']

        user = authenticate(request, username=username, password=password)

        # Неверные данные
        if user is None:
            # Возвращаем 401 Unauthorized
            response = get_response(self.action, False, 'Неверное имя пользователя или пароль!')
            return Response(status=401, data=response)

        # Авторизуем пользователя
        login(request, user)

        # Возвращаем 200 OK
        response = get_response(self.action, True, None)
        return Response(status=200, data=response)


class LogoutView(APIView):
    """APIView для выхода пользователя из системы"""
    permission_classes = (AllowAny,)
    action = 'logout'

    @handle_errors(action)
    def get(self, request, *args, **kwargs):
        logout(request)

        # Возвращаем на главную
        return HttpResponseRedirect('/')


class UsersView(APIView):
    """APIView для работы с пользователями"""
    permission_classes = (AllowAny,)
    action = 'users'

    @handle_errors(action)
    def get(self, request, *args, **kwargs):
        # TODO: можно сделать пагинацию, достаточно с фронта передать значения offset и count

        # Получаем список пользователей
        result = UserService.get_users(offset=request.GET.get('offset', 0),
                                       count=request.GET.get('count'))
        serializer = UserSerializer(result, many=True)

        # Возвращаем 200 OK
        response = get_response(self.action, True, data=serializer.data)
        return Response(status=200, data=response)


class ResumesView(APIView):
    """APIView для работы с резюме"""
    permission_classes = (AllowAny,)
    action = 'resumes'

    @handle_errors(action)
    def get(self, request, *args, **kwargs):
        # TODO: можно сделать пагинацию, достаточно с фронта передать значения offset и count

        # Получаем список резюме
        result = ResumeService.get_resumes(offset=request.GET.get('offset', 0),
                                           count=request.GET.get('count'))
        serializer = ResumeSerializer(result, many=True)

        # Возвращаем 200 OK
        response = get_response(self.action, True, data=serializer.data)
        return Response(status=200, data=response)


class ResumeView(APIView):
    """APIView для работы с резюме в личном кабинете"""
    permission_classes = (IsAuthenticated,)
    action = 'resume'

    @handle_errors(action)
    def get(self, request, *args, **kwargs):
        # Получаем резюме пользователя
        result = ResumeService.get_resume_by_user_id(request.user.id)
        serializer = ResumeSerializer(result, many=True)

        # Возвращаем 200 OK
        response = get_response(self.action, True, data=serializer.data)
        return Response(status=200, data=response)

    @handle_errors(action)
    def put(self, request, *args, **kwargs):
        # Проверяем полученные данные
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid() is False:
            return Response(status=400, data=get_response(self.action, False, serializer.errors['non_field_errors'][0]))

        # Получаем имя пользователя и пароль
        name = serializer.data['name']
        hobbies = serializer.data['hobbies']
        skills = serializer.data['skills']
        languages = serializer.data['languages']

        # Обновляем информацию
        ResumeService.edit_resume(request.user, name, hobbies, skills, languages)

        # Возвращаем 200 OK
        response = get_response(self.action, True, 'Резюме успешно сохранено!')
        return Response(status=200, data=response)
