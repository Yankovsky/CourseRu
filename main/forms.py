# coding=utf-8
from django import forms
from django.forms import ModelForm
from main.models import *


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'rows': 6, 'class': 'span6', 'placeholder': u'Текст сообщения'}
        for field in self.Meta.fields:
            self.fields[field].error_messages = {'required' : u'Необходимое поле', 'invalid': u'Некоректный формат данных'}
