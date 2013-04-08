# -*- coding: utf-8 -*-
from django.forms import widgets
from django.template.loader import render_to_string


class FileUploadWidget(widgets.FileInput):
    def render(self, name, value, attrs=None):
        # gets id if it exists
        id_part = u''
        if attrs and 'id' in attrs:
            id_part = u'id='+attrs['id']

        return render_to_string('forms/fileupload.html', {'id': id_part, 'name': name})