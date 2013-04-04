from django.forms import ModelForm, forms
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


class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ('appear_date', 'name')


class InformationForm(ModelForm):
    class Meta:
        model = Information
        fields = ('text',)

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('youtube_video_id',)

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('doc',)