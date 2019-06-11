from django.contrib import admin
from django.template.defaulttags import register
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