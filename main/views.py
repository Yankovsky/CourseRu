# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.datetime_safe import datetime
from django.utils.timezone import utc
from main.forms import FeedbackForm
from main.models import *

def index(request):
    courses = Course.objects.filter(approved=True).filter(available=True).order_by('start_date')
    return render(request, 'main/index.html', {'courses': courses})


def about(request):
    return render(request, 'main/about.html')


def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not (course.approved or course.available):
        return HttpResponseForbidden()
    return render(request, 'main/course.html', {'course': course, 'user': request.user})


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.date = datetime.utcnow().replace(tzinfo=utc)
            fb.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('main.views.index')
    else:
        form = FeedbackForm()

    return render(request, 'main/feedback.html', {
        'form': form,
    })