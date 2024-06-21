# decorators.py

from functools import wraps
from django.shortcuts import redirect

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'student':
            return redirect('login')  # or some other URL for unauthorized users
        return view_func(request, *args, **kwargs)
    return wrapper

def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'teacher':
            return redirect('login')  # or some other URL for unauthorized users
        return view_func(request, *args, **kwargs)
    return wrapper


def principal_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'principal':
            return redirect('')  # or some other URL for unauthorized users
        return view_func(request, *args, **kwargs)
    return wrapper



from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def is_principal(user):
    return user.is_authenticated and user.role == 'principal'


# def is_teacher(user):
#     return user.is_authenticated and user.role == 'teacher'


def is_student(user):
    return user.is_authenticated and user.role == 'student'