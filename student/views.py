from django.contrib.auth.decorators import permission_required, login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import utc
from django.utils.datetime_safe import datetime
from main.models import *

def student_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not (user.is_authenticated()):
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login')+"?next=%s"%request.get_full_path())
        elif not (user.userprofile.is_student()):
            return HttpResponseForbidden()
        else:
            return function(request, *args, **kw)
    return wrapper


@student_login_required
def apply_for_course(request, course_id):
    user_profile = request.user.userprofile
    course = get_object_or_404(Course, pk=course_id)

    if not (course.approved or course.available):
        return HttpResponseForbidden()

    if not (course in user_profile.courses.all()):
        user_profile.courses.add(course)
        user_profile.save()
        return HttpResponseRedirect(reverse('student.views.course', kwargs={'course_id': course_id}))
    else:
        return HttpResponseRedirect(reverse('student.views.course', kwargs={'course_id': course_id}))


@student_login_required
def course(request, course_id, template_name='student/course.html'):
    course = get_object_or_404(Course, pk=course_id)
    if course in request.user.userprofile.courses.all():
        materials = Material.objects.filter(course=course).filter(appear_date__lte=datetime.utcnow().replace(tzinfo=utc)).order_by('appear_date')
        videos = Video.objects.filter(material__in=materials)
        infos = Information.objects.filter(material__in=materials)
        documents = Document.objects.filter(material__in=materials)
        return render(request, template_name, {'course': course, 'materials': materials, 'videos': videos, 'infos': infos, 'documents': documents})
    else:
        return HttpResponseRedirect(reverse('main.views.course', kwargs={'course_id': course_id}))


@student_login_required
def courses(request, template_name='student/courses.html'):
    courses = request.user.userprofile.courses.all()
    return render(request, template_name, {'Courses': courses})
