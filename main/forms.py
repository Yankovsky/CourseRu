# coding=utf-8
from django import forms
from django.forms import ModelForm
from main.models import *


class FeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'rows': 6, 'class': 'span6', 'placeholder': u'Текст сообщения'}

    class Meta:
        model = Feedback
