from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

    def format_value(self, value):
        return value.strftime('%Y-%m-%d')


class Checkbox(forms.CheckboxInput):

    def render(self, name, value, attrs=None):
        label_on = 'Да'
        label_off = 'Нет'
        attrs['class'] = 'tgl tgl-flip'
        rendered_parent = super(Checkbox, self).render(name, value, attrs=attrs)
        return rendered_parent + '<label class="tgl-btn" data-tg-off="'+label_off+'" data-tg-on="'+\
               label_on+'" for="'+attrs['id']+'"></label>'


class FileInput(forms.FileInput):

    def render(self, name, value, attrs=None):

        rendered_parent = super(FileInput, self).render(name, value, attrs=attrs)
        return '''<label class="file-upload btn btn-info btn-sm">
                        <span>фото</span>
                    ''' + rendered_parent + '</label>'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

    def format_value(self, value):
        return value.strftime('%Y-%m-%dT%H:%i')
