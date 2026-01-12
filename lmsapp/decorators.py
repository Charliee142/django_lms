from django.http import HttpResponseForbidden
#from django.contrib.auth.models import Group
from django.shortcuts import redirect
from .models import Instructor


def instructor_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        # Check if user is authenticated and if they are an instructor
        if request.user.is_authenticated and hasattr(request.user, 'instructor'):
            return view_func(request, *args, **kwargs)
        else:
            # If not an instructor, redirect them or show a forbidden page
            return HttpResponseForbidden("You are not authorized to view this page.")
    return wrapper_func


def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=role).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have access to this page.")
        return _wrapped_view
    return decorator

@role_required('Instructor')
def instructor_dashboard(request):
    # Logic for instructor dashboard
    pass

@role_required('Student')
def student_dashboard(request):
    # Logic for student dashboard
    pass


# Add a user to the 'Student' group upon registration
#student_group = Group.objects.get(name='Student')
#user.groups.add(student_group)