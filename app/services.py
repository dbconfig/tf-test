from __future__ import annotations
from app.repositories import *
from app.specifications import *
from app.types import LanguageChoices


class UserService:
    @staticmethod
    def create_user(username: str, password: str) -> Union[User, None]:
        user = UserRepository.create(CreateUserByUsernameAndPassword(username, password))
        return user

    @staticmethod
    def is_username_exists(username: str) -> bool:
        result = UserRepository.get(UserByUsername(username))
        if result is None:
            return False
        return True

    @staticmethod
    def get_users(offset=0, count=1) -> Union[QuerySet, list]:
        return UserRepository.filter(offset=offset, count=count)


class ResumeService:
    @staticmethod
    def get_resumes(offset=0, count: int | None = None, not_empty=True) -> Union[QuerySet, list]:
        if not_empty:
            return ResumeRepository.filter(offset=offset, count=count, exclude_specification=ResumeNotEmpty())
        else:
            return ResumeRepository.filter(offset=offset, count=count)

    @staticmethod
    def get_resume_by_user_id(user_id: int) -> Union[Resume, None]:
        return ResumeRepository.get(ResumeByUserId(user_id))

    @staticmethod
    def edit_resume(user: User, name: str, hobbies: str, skills: list, languages: list) -> None:
        resume = ResumeRepository.get(ResumeByUserId(user.id))
        resume.name = name
        resume.hobbies = hobbies
        skills = list(set(skills))
        # Добавляем новые навыки
        for skill in skills:
            # Такого навыка нет - добавляем
            if not SkillRepository.filter(specification=SkillByValueAndResumeId(value=skill,
                                                                                resume_id=resume.id)).exists():
                SkillRepository.create(CreateSkill(value=skill, resume_id=resume.id))
        # Получаем список навыков, которые нужно убрать из резюме
        skills_to_set_none = SkillRepository.filter(
            specification=SkillByResumeId(resume.id),
            exclude_specification=SkillByValues(skills))
        # Ставим resume = None у всех
        for skill in skills_to_set_none:
            skill.resume = None
            SkillRepository.save(skill)
        # Добавляем новые языки
        for language in languages:
            # Такого языка нет - добавляем
            if not LanguageRepository.filter(specification=LanguageByLanguageAndResumeId(
                    language=language,
                    resume_id=resume.id)).exists():
                LanguageRepository.create(CreateLanguage(language=language, resume_id=resume.id))

        # Получаем список языков, которые нужно убрать из резюме
        languages_to_delete = LanguageRepository.filter(
            specification=LanguageByResumeId(resume.id),
            exclude_specification=LanguageByLanguages(languages))

        # Удаляем старые данные
        for language in languages_to_delete:
            LanguageRepository.delete(language)

        ResumeRepository.save(resume)


class SkillService:

    @staticmethod
    def get_skills(offset=0, count=None) -> Union[QuerySet, list]:
        return SkillRepository.filter(offset=offset, count=count)

    @staticmethod
    def get_skills_by_resume_id(resume_id: int) -> QuerySet:
        return SkillRepository.filter(specification=SkillByResumeId(resume_id))


class LanguageService:

    @staticmethod
    def get_languages(offset=0, count=1) -> list:
        # [('ru', 'Русский'), (...), ...]
        return LanguageChoices.choices

    @staticmethod
    def get_user_languages_by_resume_id(resume_id: int) -> QuerySet:
        return LanguageRepository.filter(specification=LanguageByResumeId(resume_id))
