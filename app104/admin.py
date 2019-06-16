from django.contrib import admin
from django.template.defaulttags import register
from django.db.models.functions import Length
from .models import Nosologies
from django.db.models import Q
from .views import _names



# Register your models here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key)) if dictionary.get(str(key)) else dictionary.get(key)

@register.filter
def check_user(base, username):
    if not username:
        return True
    else:
        return False

@register.filter
def get_number_by_value(row, value):
    return row.index(value)

@register.filter
def get_enumerate(data):
    return enumerate(data)

@register.filter
def is_unhiddable(data, item):
    if len(item) in [1, 2] or item == '.....':
        return True
    else:
        return False

@register.filter
def recount_rowspan_smo(data):
    nosologies = Nosologies.objects.annotate(length=Length('number')).filter(length__lte=2).order_by('id')
    return (2 + len(nosologies)) * len(data.values())


@register.filter
def recount_rowspan_mo(data):
    nosologies = Nosologies.objects.annotate(length=Length('number')).filter(length__lte=2).order_by('id')
    return 2 + len(nosologies)


@register.filter
def display_item(row):
    if len(row[0]) <= 2:
        return 'table-cell'
    else:
        return 'none'

@register.filter
def display_row(row):
    if len(row[0]) <= 2:
        return 'table-row'
    else:
        return 'none'

@register.filter
def get_id_by_name(data, name):
    for k, v in _names.items():
        if v == name:
            return k
    return name

@register.filter
def get_id(row):
    return row[0][0]

