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
            else:
                id_part = mark_safe(u'id=' + id_part)

        return render_to_string('forms/fileupload.html', {'id': id_part, 'name': name})


class DateTimeWidget(widgets.DateTimeInput):
    def __init__(self, picker_id=None, *args, **kwargs):
        super(widgets.DateTimeInput, self).__init__(*args, **kwargs)
        self.picker_id = picker_id

    def render(self, name, value, attrs=None):
        # gets id if it exists
        id_part = u''
        if attrs and 'id' in attrs:
            id_part = attrs['id']
            if (id_part[0] != '"'):
                id_part = mark_safe(u'id="' + id_part + u'"')
            else:
                id_part = mark_safe(u'id=' + id_part)

        # gets widget id
        if self.picker_id is None:
            self.picker_id = u'datetimepicker1'

        # handle value
        if value is None:
            value = u''

        return render_to_string('forms/datetime.html', {'id': id_part, 'name': name, 'value': value, 'picker_id': self.picker_id})


class DateWidget(widgets.DateInput):
    def __init__(self, picker_id=None, *args, **kwargs):
        super(widgets.DateInput, self).__init__(*args, **kwargs)
        self.picker_id = picker_id

    def render(self, name, value, attrs=None):
        # gets id if it exists
        id_part = u''
        if attrs and 'id' in attrs:
            id_part = attrs['id']
            if (id_part[0] != '"'):
                id_part = mark_safe(u'id="' + id_part + u'"')
            else:
                id_part = mark_safe(u'id=' + id_part)

        # gets widget id
        if self.picker_id is None:
            self.picker_id = u'datepicker1'

        # handle value
        if value is None:
            value = u''

        return render_to_string('forms/date.html', {'id': id_part, 'name': name, 'value': value, 'picker_id': self.picker_id})