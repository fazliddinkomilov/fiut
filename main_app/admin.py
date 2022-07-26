from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from modeltranslation.admin import TranslationAdmin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


class MainAdminForm(forms.ModelForm):
    title_ru = forms.CharField(label="Название", widget=CKEditorUploadingWidget())
    title_en = forms.CharField(label="Название", widget=CKEditorUploadingWidget())
    title_uz = forms.CharField(label="Название", widget=CKEditorUploadingWidget())
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_uz = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    name_ru = forms.CharField(label="name", widget=CKEditorUploadingWidget())
    name_en = forms.CharField(label="name", widget=CKEditorUploadingWidget())
    name_uz = forms.CharField(label="исим", widget=CKEditorUploadingWidget())



admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Student)

admin.site.register(Session)


@admin.register(News)
class News(TranslationAdmin):
    list_display = ("title", "description", "image", "registrationlink")


@admin.register(Subject)
class Subject(TranslationAdmin):
    list_display = ("name",)
    list_display_links = ("name",)


@admin.register(Course)
class Course(TranslationAdmin):
    list_display = ("name",)
    list_display_links = ("name",)


admin.site.register(HR)
