# core/decorators.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'teacher'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view

def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'student'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view
