from django.db.models import TextChoices


class LanguageChoices(TextChoices):
    ru = 'ru', 'Русский'
    en = 'en', 'Английский'
    uk = 'uk', 'Украинский'
    be = 'be', 'Белорусский'
    zn = 'zn', 'Китайский'
