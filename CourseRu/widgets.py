# -*- coding: utf-8 -*-
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class FileUploadWidget(widgets.FileInput):
    def render(self, name, value, attrs=None):
        # gets id if it exists
        id_part = u''
        if attrs and 'id' in attrs:
            id_part = attrs['id']
            if (id_part[0] != '"'):
                id_part = mark_safe(u'id="' + id_part + u'"')

        return render_to_string('forms/fileupload.html', {'id': id_part, 'name': name})

