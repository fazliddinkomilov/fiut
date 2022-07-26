from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Subject)
class SubjectTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name',)
