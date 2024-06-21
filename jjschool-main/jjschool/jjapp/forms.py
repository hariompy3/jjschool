from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

from django import forms
from .models import Teacher, CustomUser

class CustomUserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'role', 'password1', 'password2', 'first_name', 'last_name', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class PrincipalForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')
#


class TeacherLogForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class StudentLogForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']















class TeacherPriForm(forms.ModelForm):
    class Meta:
        model = Teacher 
        fields = [ 'phone_number', 'class_teacher_of_grade',"main_subject","extra_subjects", 'address',  'date_of_birth']


# forms.py
from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'class_teacher_of_grade']


# class SudentForm(AuthenticationForm):
#     class Meta:
#         fields = ('username', 'password')

from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name', 'level']  # Include 'level' in the form


# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['student', 'status']



# class TeacherPriForm(AuthenticationForm):
#     class Meta:
#         model = Teacher
#         fields = ['username', 'password', 'name', 'email', 'class_teacher_of_grade', 'main_subject', 'extra_subjects']
       
       

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'first_name', 'last_name', 'date_of_birth', "adhar_num", 'admission_date', 'grade',  'total_fee', 'remaining_fee']







from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'status']

    def _init_(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super(AttendanceForm, self)._init_(*args, **kwargs)
        if teacher:
            self.fields['student'].queryset = Student.objects.filter(grade=teacher.class_teacher_of_grade)






from django import forms
from .models import Student, CustomUser

class AadhaarForm(forms.Form):
    adhar_num = forms.CharField(max_length=12, label="Aadhaar Number")

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['adhar_num', 'date_of_birth', 'grade']

class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['topic', 'description']

class ComplaintResolutionForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['is_resolved' ]










from django import forms
from .models import Classroom, Subject, TeacherSubjectAssignment

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'grade', 'capacity', 'class_teacher', 'teachers']

# jjapp/forms.py
# jjapp/forms.py
from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

from django import forms
from .models import Teacher, TeacherSubjectAssignment

class TeacherSubjectForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjectAssignment
        fields = ['teacher', 'subject']

    def _init_(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        super(TeacherSubjectForm, self)._init_(*args, **kwargs)
        if self.teacher:
            self.fields['teacher'].queryset = Teacher.objects.filter(pk=self.teacher.pk)
            self.fields['teacher'].initial = self.teacher





from django import forms
from .models import Subject

class PrincipalSubjectForm(forms.Form):
    subject_name = forms.CharField(max_length=255)
    
    def add_subject(self, grade):
        subject_name = self.cleaned_data['subject_name']
        subject, created = Subject.objects.get_or_create(name=subject_name, grade=grade)
        return subject

from django import forms
from .models import Teacher, Grade, Subject, TeacherSubjectAssignment

class TeacherSubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjectAssignment
        fields = ['teacher', 'grade', 'subject']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get('grade')
        if grade:
            self.fields['subject'].queryset = Subject.objects.filter(grade=grade)
        return cleaned_data




# jjapp/forms.py

from django import forms
from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'classroom', 'attendance_percentage', 'adhar_num', 'profile_photo']

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.required = False

# jjapp/forms.py

from django import forms
from .models import Student

class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'profile_photo', 'performance']
