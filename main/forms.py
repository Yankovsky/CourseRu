# coding=utf-8
from django import forms
from django.forms import ModelForm
from main.models import *

class AddCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'admin_summary')

    def clean_name(self):
        name = self.cleaned_data['name']
        courses_found = Course.objects.filter(name__iexact=name)

        if len(courses_found) >= 1:
            raise forms.ValidationError('Name already in use in another course')

        return name

class EditCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('short_summary', 'description', 'organisation', 'logo', 'start_date', 'end_date', )


class FeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'rows': 6, 'class': 'span6', 'placeholder': u'Текст сообщения'}

    class Meta:
        model = Feedback

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ('course', 'upload_date')