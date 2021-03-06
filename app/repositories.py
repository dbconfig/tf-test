from typing import Union
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from app.models import Resume, Skill, Language
from app.specifications import Specification, CreateSpecification


class Repository:
    """Дополнительный слой абстракции для взаимодействия с данными"""

    @staticmethod
    def get(specification: Specification = Specification()) -> Union[object, None]:
        raise NotImplementedError()

    @staticmethod
    def create(specification: CreateSpecification = Specification()) -> Union[object, None]:
        pass

    @staticmethod
    def save(obj: object) -> None:
        pass

    @staticmethod
    def filter(specification: Specification = Specification()) -> object:
        pass

    @staticmethod
    def all() -> object:
        pass


class UserRepository(Repository):
    """Слой абстракции для взаимодействия с таблицей пользователей в базе данных"""

    @staticmethod
    def get(specification: Specification = Specification()) -> Union[User, None]:
        try:
            return User.objects.get(**specification.is_satisfied())
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(specification: CreateSpecification = CreateSpecification()) -> Union[User, None]:
        obj = User.objects.create_user(**specification.values())
        return obj

    @staticmethod
    def save(obj: User, update_fields=None) -> None:
        obj.save(update_fields=update_fields)

    @staticmethod
    def filter(offset=0, count=None, order_by='pk', specification: Specification = Specification()) -> QuerySet:
        result = User.objects.filter(**specification.is_satisfied()).order_by(order_by)
        if count is None:
            return result
        return result[offset:count]

    @staticmethod
    def all() -> QuerySet:
        return User.objects.all()


class ResumeRepository(Repository):
    """Слой абстракции для взаимодействия с таблицей резюме в базе данных"""

    @staticmethod
    def get(specification: Specification = Specification()) -> Union[Resume, None]:
        try:
            return Resume.objects.get(**specification.is_satisfied())
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(specification: CreateSpecification = CreateSpecification()) -> Union[Resume, None]:
        obj = Resume(**specification.values())
        ResumeRepository.save(obj)
        return obj

    @staticmethod
    def save(obj: Resume, update_fields=None) -> None:
        obj.save(update_fields=update_fields)

    @staticmethod
    def filter(offset=0, count=None, order_by='pk',
               exclude_specification: Specification = Specification(),
               specification: Specification = Specification()) -> QuerySet:
        result = Resume.objects.filter(**specification.is_satisfied()).order_by(order_by)
        result = result.exclude(**exclude_specification.is_satisfied())
        if count is None:
            return result
        return result[offset:count]

    @staticmethod
    def all() -> QuerySet:
        return Resume.objects.all()


class SkillRepository(Repository):
    """Слой абстракции для взаимодействия с таблицей навыков в базе данных"""

    @staticmethod
    def get(specification: Specification = Specification()) -> Union[Skill, None]:
        try:
            return Skill.objects.get(**specification.is_satisfied())
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(specification: CreateSpecification = CreateSpecification()) -> Union[Skill, None]:
        obj = Skill(**specification.values())
        SkillRepository.save(obj)
        return obj

    @staticmethod
    def save(obj: Skill, update_fields=None) -> None:
        obj.save(update_fields=update_fields)

    @staticmethod
    def filter(offset=0, count=None, order_by='pk',
               exclude_specification: Specification = Specification(),
               specification: Specification = Specification()) -> QuerySet:
        result = Skill.objects.filter(**specification.is_satisfied()).order_by(order_by)
        result = result.exclude(**exclude_specification.is_satisfied())
        if count is None:
            return result
        return result[offset:count]

    @staticmethod
    def all() -> QuerySet:
        return Skill.objects.all()


class LanguageRepository(Repository):
    """Слой абстракции для взаимодействия с таблицей языков в базе данных"""

    @staticmethod
    def get(specification: Specification = Specification()) -> Union[Language, None]:
        try:
            return Language.objects.get(**specification.is_satisfied())
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(specification: CreateSpecification = CreateSpecification()) -> Union[Language, None]:
        obj = Language(**specification.values())
        LanguageRepository.save(obj)
        return obj

    @staticmethod
    def save(obj: Language, update_fields=None) -> None:
        obj.save(update_fields=update_fields)

    @staticmethod
    def filter(offset=0, count=None, order_by='pk',
               exclude_specification: Specification = Specification(),
               specification: Specification = Specification()) -> QuerySet:
        result = Language.objects.filter(**specification.is_satisfied()).order_by(order_by)
        result = result.exclude(**exclude_specification.is_satisfied())
        if count is None:
            return result
        return result[offset:count]

    @staticmethod
    def all() -> QuerySet:
        return Language.objects.all()

    @staticmethod
    def delete(obj: Language) -> None:
        obj.delete()
