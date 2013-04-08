import time
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import utc
from django.utils.datetime_safe import datetime
from main.forms import *
from forms import *

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
def put_course(request, course_id, post_put_course_redirect=None):
    course = get_object_or_404(Course, pk=course_id)

    if not course.approved:
        return HttpResponseForbidden()

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if course.available:
        return HttpResponseForbidden()

    course.available = True
    course.save()

    if post_put_course_redirect is None:
        post_put_course_redirect = reverse('instructor.views.course', kwargs={'course_id': course.id})

    return HttpResponseRedirect(post_put_course_redirect)

@instructor_login_required
def add_course(request, template_name='instructor/addcourse.html', add_course_form=AddCourseForm,
               post_course_new_redirect=None):
    if request.method == 'POST':
        form = add_course_form(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.date = datetime.utcnow().replace(tzinfo=utc)
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

    if course in request.user.userprofile.courses.all():
        materials = Material.objects.filter(course=course).order_by('-appear_date')
        videos = Video.objects.filter(material__in=materials).order_by('-material__appear_date')
        infos = Information.objects.filter(material__in=materials).order_by('-material__appear_date')
        documents = Document.objects.filter(material__in=materials).order_by('-material__appear_date')
        userprofiles = course.userprofile_set.all()
        users = [userprofile.user for userprofile in userprofiles]
        return render(request, template_name, {'course': course, 'materials': materials, 'videos': videos, 'infos': infos, 'files': documents, 'users': users})
    else:
        return HttpResponseRedirect(reverse('main.views.course', kwargs={'course_id': course_id}))


@instructor_login_required
def courses(request, template_name='instructor/courses.html'):
    courses = request.user.userprofile.courses.filter(approved=True).filter(available=True)
    approved = request.user.userprofile.courses.filter(approved=True).filter(available=False)
    requests = request.user.userprofile.courses.filter(approved=False)
    return render(request, template_name, {'Courses': courses, 'Requests': requests, 'Approved': approved})


@instructor_login_required
def add_news(request, course_id, template_name="instructor/addinfo.html", post_add_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form1 = MaterialForm(request.POST)
        form2 = InformationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            material = form1.save(commit=False)
            info = form2.save(commit=False)
            material.author = request.user
            material.date = datetime.utcnow().replace(tzinfo=utc)
            material.course = course
            material.save()
            info.material = material
            info.save()

            if post_add_information_redirect is None:
                post_add_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

            return HttpResponseRedirect(post_add_information_redirect)
    else:
        form1 = MaterialForm()
        form2 = InformationForm()

    return render(request, template_name, {'course': course, 'form1': form1, 'form2': form2})


@instructor_login_required
def edit_news(request, course_id, info_id, template_name="instructor/editinfo.html", post_edit_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)
    info = get_object_or_404(Information, pk=info_id)
    material = info.material

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form1 = MaterialForm(request.POST, instance=material)
        form2 = InformationForm(request.POST, instance=info)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()

            if post_edit_information_redirect is None:
                post_edit_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

            return HttpResponseRedirect(post_edit_information_redirect)
    else:
        form1 = MaterialForm(instance=material)
        form2 = InformationForm(instance=info)

    return render(request, template_name, {'course': course, 'form1': form1, 'form2': form2})


@instructor_login_required
def delete_news(request, course_id, info_id, post_delete_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)
    info = get_object_or_404(Information, pk=info_id)
    material = info.material

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    material.delete()

    if post_delete_information_redirect is None:
        post_delete_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

    return HttpResponseRedirect(post_delete_information_redirect)

# # # # #
# # # # #

@instructor_login_required
def add_video(request, course_id, template_name="instructor/addinfo.html", post_add_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form1 = MaterialForm(request.POST)
        form2 = VideoForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            material = form1.save(commit=False)
            video = form2.save(commit=False)
            material.author = request.user
            material.date = datetime.utcnow().replace(tzinfo=utc)
            material.course = course
            material.save()
            video.material = material
            video.save()

            if post_add_information_redirect is None:
                post_add_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

            return HttpResponseRedirect(post_add_information_redirect)
    else:
        form1 = MaterialForm()
        form2 = VideoForm()

    return render(request, template_name, {'course': course, 'form1': form1, 'form2': form2})


@instructor_login_required
def edit_video(request, course_id, video_id, template_name="instructor/editinfo.html", post_edit_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)
    video = get_object_or_404(Video, pk=video_id)
    material = video.material

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form1 = MaterialForm(request.POST, instance=material)
        form2 = VideoForm(request.POST, instance=video)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()

            if post_edit_information_redirect is None:
                post_edit_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

            return HttpResponseRedirect(post_edit_information_redirect)
    else:
        form1 = MaterialForm(instance=material)
        form2 = VideoForm(instance=video)

    return render(request, template_name, {'course': course, 'form1': form1, 'form2': form2})


@instructor_login_required
def delete_video(request, course_id, video_id, post_delete_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)
    video = get_object_or_404(Video, pk=video_id)
    material = video.material

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    material.delete()

    if post_delete_information_redirect is None:
        post_delete_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

    return HttpResponseRedirect(post_delete_information_redirect)

# # # # #
# # # # #

@instructor_login_required
def add_file(request, course_id, template_name="instructor/addinfo.html", post_add_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form1 = MaterialForm(request.POST, request.FILES)
        form2 = DocumentForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            material = form1.save(commit=False)
            file = form2.save(commit=False)
            material.author = request.user
            material.date = datetime.utcnow().replace(tzinfo=utc)
            material.course = course
            material.save()
            file.material = material
            file.save()

            if post_add_information_redirect is None:
                post_add_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

            return HttpResponseRedirect(post_add_information_redirect)
    else:
        form1 = MaterialForm()
        form2 = DocumentForm()

    return render(request, template_name, {'course': course, 'form1': form1, 'form2': form2})


@instructor_login_required
def edit_file(request, course_id, file_id, template_name="instructor/editinfo.html", post_edit_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)
    file = get_object_or_404(Document, pk=file_id)
    material = file.material

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    if request.method == 'POST':
        form1 = MaterialForm(request.POST, instance=material)
        form2 = DocumentForm(request.POST, request.FILES, instance=file)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()

            if post_edit_information_redirect is None:
                post_edit_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

            return HttpResponseRedirect(post_edit_information_redirect)
    else:
        form1 = MaterialForm(instance=material)
        form2 = DocumentForm(instance=file)

    return render(request, template_name, {'course': course, 'form1': form1, 'form2': form2})


@instructor_login_required
def delete_file(request, course_id, file_id, post_delete_information_redirect=None):
    course = get_object_or_404(Course, pk=course_id)
    file = get_object_or_404(Document, pk=file_id)
    material = file.material

    if not course in request.user.userprofile.courses.all():
        return HttpResponseForbidden()

    material.delete()

    if post_delete_information_redirect is None:
        post_delete_information_redirect = reverse('instructor.views.course', kwargs={'course_id': course_id})

    return HttpResponseRedirect(post_delete_information_redirect)
