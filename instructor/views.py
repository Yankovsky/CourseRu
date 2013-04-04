import time
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.utils.timezone import utc
from django.utils.datetime_safe import datetime
from main.forms import *
from main.models import *

def instructor_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not (user.is_authenticated()):
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login')+"?next=%s"%request.get_full_path())
        elif not (user.userprofile.is_instructor()):
            return HttpResponseForbidden()
        else:
            return function(request, *args, **kw)
    return wrapper


@instructor_login_required
def add_course(request, template_name='instructor/addcourse.html', add_course_form=AddCourseForm,
               post_course_new_redirect=None):
    if request.method == 'POST':
        form = add_course_form(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.date = time.strftime("%Y-%m-%d %H:%M:%S")
            course.approved = False
            course.save()
            request.user.userprofile.courses.add(course) # # # # #
            if post_course_new_redirect is None:
                post_course_new_redirect = reverse('instructor.views.course', kwargs={'course_id': course.id})
            return HttpResponseRedirect(post_course_new_redirect)
    else:
        form = add_course_form()
    return render(request, template_name, {'form': form})


@instructor_login_required
def edit_course(request, course_id, template_name='instructor/editcourse.html', edit_course_form=EditCourseForm,
                post_course_edit_redirect=None):

    course = get_object_or_404(Course, pk=course_id)

    if not course.approved:
        return HttpResponseForbidden()

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = edit_course_form(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()

            if post_course_edit_redirect is None:
                post_course_edit_redirect = reverse('instructor.views.course', kwargs={'course_id': course.id})
            return HttpResponseRedirect(post_course_edit_redirect)
    else:
        form = edit_course_form(instance=course)
    return render(request, template_name, {'form': form})

@instructor_login_required
def delete_course(request, course_id, post_delete_course_redirect=None):
    course = get_object_or_404(Course, pk=course_id)

    if not (course in request.user.userprofile.courses.all()):
        return HttpResponseForbidden()

    course.delete()

    if post_delete_course_redirect is None:
        post_delete_course_redirect = reverse('instructor.views.courses')

    return HttpResponseRedirect(post_delete_course_redirect)

@instructor_login_required
def course(request, course_id, template_name='instructor/course.html'):
    course = get_object_or_404(Course, pk=course_id)
    # show materials: documents, videos, infos
    if course in request.user.userprofile.courses.all():
        materials = Material.objects.filter(course=course).filter(appear_date__lte=datetime.utcnow().replace(tzinfo=utc)).order_by('appear_date')
        videos = Video.objects.filter(material__in=materials)
        infos = Video.objects.filter(material__in=materials)
        documents = Video.objects.filter(material__in=materials)
        return render(request, template_name, {'course': course, 'materials': materials, 'videos': videos, 'infos': infos, 'documents': documents})
    else:
        return HttpResponseRedirect(reverse('main.views.course', kwargs={'course_id': course_id}))


@instructor_login_required
def courses(request, template_name='instructor/courses.html'):
    courses = request.user.userprofile.courses.filter(approved=True).filter(available=True)
    approved = request.user.userprofile.courses.filter(approved=True).filter(available=False)
    requests = request.user.userprofile.courses.filter(approved=False)
    return render(request, template_name, {'Courses': courses, 'Requests': requests, 'Approved': approved})


# upload videos, materials, infos
@instructor_login_required
def upload(request, course_id, template_name='instructor/upload.html'):
    course = get_object_or_404(Course, pk=course_id)

    if not (course in request.user.userprofile.courses.all()):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.course = course
            doc.upload_date = datetime.utcnow().replace(tzinfo=utc)
            doc.save()
            return HttpResponseRedirect(reverse('instructor.views.upload', kwargs={'course_id': course.id}))
    else:
        form = DocumentForm()

    documents = Document.objects.filter(course=course).order_by('appear_date')
    return render(request, template_name, {'documents': documents, 'form': form, 'course': course})
