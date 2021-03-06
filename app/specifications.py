from django.contrib.auth.models import User


class Specification:
    """Спецификация для взаимодействия с репозиторием: получение данных"""

    def is_satisfied(self) -> dict:
        return {}


class CreateSpecification:
    """Спецификация для взаимодействия с репозиторием: создание объекта"""

    def values(self) -> dict:
        return {}


class IsUserAutenticated(Specification):
    __slots__ = ('user',)

    def __init__(self, user: User):
        self.user = user

    def is_satisfied(self) -> bool:
        return self.user.is_authenticated


class UserByUsername(Specification):
    __slots__ = ('username',)

    def __init__(self, username: str):
        self.username = username

    def is_satisfied(self):
        return {
            'username__exact': self.username,
        }


class ResumeNotEmpty(Specification):
    def is_satisfied(self) -> dict:
        return {
            'name__exact': '',
            'hobbies__exact': '',
        }


class ResumeByUserId(Specification):
    __slots__ = ('user_id',)

    def __init__(self, user_id: int):
        self.user_id = user_id

    def is_satisfied(self):
        return {
            'user_id__exact': self.user_id,
        }


class SkillByResumeId(Specification):
    __slots__ = ('resume_id',)

    def __init__(self, resume_id: int):
        self.resume_id = resume_id

    def is_satisfied(self):
        return {
            'resume_id__exact': self.resume_id,
        }


class SkillByValues(Specification):
    __slots__ = ('values',)

    def __init__(self, values: list):
        self.values = values

    def is_satisfied(self):
        return {
            'value__in': self.values,
        }


class SkillByValueAndResumeId(Specification):
    __slots__ = ('value', 'resume_id',)

    def __init__(self, value: str, resume_id: int):
        self.value = value
        self.resume_id = resume_id

    def is_satisfied(self):
        return {
            'value__exact': self.value,
            'resume_id__exact': self.resume_id,
        }


class CreateSkill(CreateSpecification):
    __slots__ = ('value', 'resume_id',)

    def __init__(self, value: str, resume_id: int):
        self.value = value
        self.resume_id = resume_id

    def values(self):
        return {
            'value': self.value,
            'resume_id': self.resume_id,
        }


class LanguageByResumeId(Specification):
    __slots__ = ('resume_id',)

    def __init__(self, resume_id: int):
        self.resume_id = resume_id

    def is_satisfied(self):
        return {
            'resume_id__exact': self.resume_id,
        }


class LanguageByLanguageAndResumeId(Specification):
    __slots__ = ('language', 'resume_id',)

    def __init__(self, language: str, resume_id: int):
        self.language = language
        self.resume_id = resume_id

    def is_satisfied(self):
        return {
            'language__exact': self.language,
            'resume_id__exact': self.resume_id,
        }


class LanguageByLanguages(Specification):
    __slots__ = ('languages',)

    def __init__(self, languages: list):
        self.languages = languages

    def is_satisfied(self):
        return {
            'language__in': self.languages,
        }


class CreateLanguage(CreateSpecification):
    __slots__ = ('language', 'resume_id',)

    def __init__(self, language: str, resume_id: int):
        self.language = language
        self.resume_id = resume_id

    def values(self):
        return {
            'language': self.language,
            'resume_id': self.resume_id,
        }


class CreateUserByUsernameAndPassword(CreateSpecification):
    __slots__ = ('username', 'password')

    def __init__(self, username: str, password: str = None):
        self.username = username
        self.password = password

    def values(self):
        return {
            'username': self.username,
            'password': self.password,
        }
