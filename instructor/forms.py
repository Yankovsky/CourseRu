# -*- coding: utf-8 -*-
from django.forms import ModelForm, forms
from main.models import *

class AddCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'admin_summary')

    def __init__(self, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required' : u'Необходимое поле', 'invalid': u'Некоректный формат данных'}

    def clean_name(self):
        name = self.cleaned_data['name']
        courses_found = Course.objects.filter(name__iexact=name)

        if len(courses_found) >= 1:
            raise forms.ValidationError(u'Курс с таким названием уже существует')

        return name


class EditCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('short_summary', 'description', 'organisation', 'logo', 'start_date', 'end_date', )
        required = ('short_summary', 'description', 'organisation', 'start_date', 'end_date')

    # def clean_short_summary(self):
    #     short_summary = self.cleaned_data['short_summary'].strip()
    #     if short_summary == '':
    #         raise forms.ValidationError(u'Необходимое поле')
    #     return short_summary

    def __init__(self, *args, **kwargs):
        super(EditCourseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required' : u'Необходимое поле', 'invalid': u'Некоректный формат данных'}
        for field in self.Meta.required:
            self.fields[field].required = True

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ('appear_date', 'name')

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required' : u'Необходимое поле', 'invalid': u'Некоректный формат данных'}


class InformationForm(ModelForm):
    class Meta:
        model = Information
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(InformationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required' : u'Необходимое поле', 'invalid': u'Некоректный формат данных'}

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('youtube_video_id',)

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required' : u'Необходимое поле', 'invalid': u'Некоректный формат данных'}

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('doc',)

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required' : u'Необходимое поле', 'invalid': u'Некоректный формат данных'}