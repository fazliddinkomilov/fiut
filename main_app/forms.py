from django import forms
from django.forms.widgets import DateInput, TextInput
from modeltranslation.admin import TranslationAdmin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from translated_fields.utils import language_code_formfield_callback
from django.utils.translation import gettext_lazy as _


class FormSettings(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def save(self):
        obj = super(Subject, self).save(commit=False)
        obj.save()
        self.save_m2m()
        return obj


class CustomUserForm(FormSettings):
    email = forms.EmailField(label=_('email'), required=True)
    gender = forms.ChoiceField(label=_('gender'), choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(label=_('first_name'), required=True)
    last_name = forms.CharField(label=_('last_name'), required=True)
    address = forms.CharField(label=_('address'), widget=forms.Textarea)
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField(label=_('profile_pic'))

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender', 'password', 'profile_pic', 'address']


class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + \
                 ['course', 'session', 'nationality', 'date_of_birth', _('phone_number'), 'home_number', 'nationality',
                  'marital_status', 'education_pay_type', 'course_level', 'location_type_name', 'admission_date', 'ITN',
                  'passport_picture_front', 'passport_picture_back']

        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'admission_date': DateInput(attrs={'type': 'date'}),
        }


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + \
                 ['course', 'nationality', 'date_of_birth', _('phone_number'), 'home_number', 'nationality',
                  'marital_status', 'location_type_name', 'ITN', 'passport_picture_front', 'passport_picture_back']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }


class HRForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HRForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = HR
        fields = CustomUserForm.Meta.fields + \
                 ['nationality', 'date_of_birth', _('phone_number'), 'home_number', 'nationality',
                  'marital_status', 'location_type_name', 'ITN', 'passport_picture_front', 'passport_picture_back']

        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }


class NewsForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = News
        fields = ['title_en', 'title_ru', 'title_uz', 'description_en', 'description_ru', 'description_uz', 'image', "registrationlink"]


class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = ['name_en', 'name_ru', 'name_uz']


class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name_en', 'name_ru', 'name_uz', 'staff', 'course']


class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = ['start_year', 'end_year']
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportHRForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportHRForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportHR
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class FeedbackHRForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackHRForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackHR
        fields = ['feedback']


class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStudentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']


class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)


class HREditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HREditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = HR
        fields = CustomUserForm.Meta.fields


class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentResult
        fields = ['session_year', 'subject', 'student', 'test', 'exam']
