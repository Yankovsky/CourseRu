from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render
from main.models import *

def staff_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not (user.is_authenticated()):
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login')+"?next=%s"%request.get_full_path())
        elif not (user.is_staff):
            return HttpResponseForbidden()
        else:
            return function(request, *args, **kw)
    return wrapper

@staff_login_required
def index(request, template_name='control/index.html'):
    return render(request, template_name)

@staff_login_required
def courses(request, template_name='control/courses.html'):
    requests = Course.objects.filter(approved=False)
    return render(request, template_name, {'requests': requests})

@staff_login_required
def feedbacks(request, template_name='control/feedbacks.html'):
    feedbacks = Feedback.objects.all()
    return render(request, template_name, {'feedbacks': feedbacks})

@staff_login_required
def approve(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.approved = True
    return HttpResponseRedirect(reverse('control.views.courses'))