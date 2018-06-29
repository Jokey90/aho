from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def image(file, max_size=300):
    from main import settings
    if file:
        title = '<img src="/' + settings.MEDIA_URL + str(file) + '" style="max-width: '+str(max_size)+'px; max-width: '+str(max_size)+'px;"/>'
        return image_link(file, title)
    else:
        return ''


@register.simple_tag
def image_link(file, title='Просмотр', classes=''):
    from main import settings
    from PIL import Image
    import os

    if file:
        width = 1000
        height = 800
        try:
            f = Image.open(os.path.join(settings.MEDIA_ROOT,str(file)))
            width, height = f.size
            ratio = width / height
            if width > 1000:
                width = 1000
                height = width / ratio
            elif height > 800:
                height = 800
                width = height * ratio
        except IOError:
            pass
        html = '<a href="#" class="'+classes+'" onclick=\''
        html += ' window.open("/' + settings.MEDIA_URL + str(file) + '", "_blank", "toolbar=no,scrollbars=yes,resizable=yes,top=50,left=100,width='+str(width)+',height='+str(height)+'"); '
        html += ' return false; '
        html += '\'>'+title+'</a>'
        return format_html(html)
    else:
        return ''


@register.simple_tag
def get_label(instance, field_name):
    if instance:
        #try:
        return instance._meta.get_field(field_name).verbose_name
        #except:
        #    return None
    else:
        return None


@register.simple_tag
def month(month):
    if month != '':
        from main.structures import MONTHS
        return MONTHS[int(month)-1][1]
    else:
        return ''


@register.filter
def num(value, precision=2):
    if value:
        return ("{:,."+str(precision)+"f}").format(value).replace(',', ' ').replace('.',',')
    else:
        return ''


@register.filter
def rub(value):
    if value:
        return "{:,.2f}".format(value).replace(',', ' ').replace('.',',')+' руб.'
    else:
        return ''


@register.filter
def boolean(value):
    if value:
        return 'Да'
    else:
        return 'Нет'


@register.filter
def empty(value):
    if value is not None:
        return value
    else:
        return ''


@register.inclusion_tag('main/paginator.html', takes_context=True)
def paginator(context, paginated_list):
    if 'is_mobile' in context:
        return {'list': paginated_list, 'is_mobile': context['is_mobile']}
    else:
        return {'list': paginated_list}


@register.inclusion_tag('form.html', takes_context=True)
def table_form(context, form_var, rows_only=False):
    if 'is_mobile' in context:
        return {'form': form_var, 'rows_only': rows_only, 'is_mobile': context['is_mobile']}
    else:
        return {'form': form_var, 'rows_only': rows_only}


@register.filter
def expire(value, days):
    from datetime import date, timedelta
    if isinstance(value, date):
        if value < date.today():
            return format_html('<span class="date-expired">'+value.strftime('%d.%m.%Y')+'</span>')
        elif value - timedelta(days=days) < date.today():
            return format_html('<span class="date-expiring">'+value.strftime('%d.%m.%Y')+'</span>')
        else:
            return value.strftime('%d.%m.%Y')


@register.filter
def spaces(value):
    value_str = str(value)
    strlen = len(value_str)
    if strlen > 0:
        comma_position = value_str.find(',')
        if comma_position > 3:
            for i in range(3, comma_position, 3):
                value_str = value_str[0:comma_position-i]+' '+value_str[comma_position-i:]
        elif comma_position < 0:
            if strlen > 3:
                for i in range(3, strlen, 3):
                    value_str = value_str[0:strlen - i] + ' ' + value_str[strlen - i:]
        return value_str
    else:
        return ''


@register.filter
def sum_vals(array, field_name):
    return sum([getattr(elem, field_name) for elem in array])


@register.filter
def count_vals(array, field_name):
    return sum([1 for elem in array if getattr(elem, field_name)])


@register.filter
def cut_length(value, length=50):
    if len(value) > length:
        return value[:length]+'...'
    else:
        return value
