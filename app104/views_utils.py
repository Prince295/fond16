# -*- coding: utf-8 -*-

from django.utils import timezone
from dateutil import relativedelta


def copy_data(result, copied, smo_list, mo_list):
    u"""
    затычка, чтобы избежать потери данных
    :param result: структура, которую меняем,
    :param copied: структура, которую необходимо разбить на части
    :param smo_list: список запрашиваемых страховых компаний
    :param mo_list: список запрашиваемых муниципальных организаций
    :return: dict
    """
    for k, v in copied.items():
        if str(k) in smo_list or k in smo_list:
            result[k] = {}
            for kk, vv in v.items():
                if str(kk) in mo_list or kk in mo_list:
                    result[k][kk] = []
                    for num, it in enumerate(vv):
                        result[k][kk].append([])
                        for i in it:
                            result[k][kk][num].append(0)
    return result


def get_column(new, old):
    u"""Возвращает строковое отображение колонки"""
    new = int(new)
    old = int(old)
    if old != 0:
        result = 100 * (new - old)/old
        result = round(result, 2)
    else:
        if new != 0:
            result = 'new'
        else:
            result = 0.00
    return u'{} %'.format(str(result))

def calculate_date(args):
    u"""
    возвращает промежуток дат рождения для запроса
    :return:
    """
    if len(args) > 0:
        if args[0] =='adult':
            date_begin = timezone.datetime.now() + relativedelta.relativedelta(years=-60, months=-11, days=-31)
            date_end = timezone.datetime.now() + relativedelta.relativedelta(years=-18)
            return ['{year}-{month}-{day}'.format(year=date_begin.year, month=date_begin.month, day=date_begin.day),
                    '{year}-{month}-{day}'.format(year=date_end.year, month=date_end.month, day=date_end.day)]
        elif args[0] == 'pensioners':
            date_begin = timezone.now() + relativedelta.relativedelta(years=-170)
            date_end = timezone.now() + relativedelta.relativedelta(years=-61)
            return ['{year}-{month}-{day}'.format(year=date_begin.year, month=date_begin.month, day=date_begin.day),
                    '{year}-{month}-{day}'.format(year=date_end.year, month=date_end.month, day=date_end.day)]
        elif args[0] == 'babies':
            date_begin = timezone.now() + relativedelta.relativedelta(years=-1)
            date_end = timezone.now()
            return ['{year}-{month}-{day}'.format(year=date_begin.year, month=date_begin.month, day=date_begin.day),
                    '{year}-{month}-{day}'.format(year=date_end.year, month=date_end.month, day=date_end.day)]
        elif args[0] == 'child':
            date_begin = timezone.now() + relativedelta.relativedelta(years=-17, months=-11, days=-31)
            date_end = timezone.now() + relativedelta.relativedelta(years=-1)
            return ['{year}-{month}-{day}'.format(year=date_begin.year, month=date_begin.month, day=date_begin.day),
                    '{year}-{month}-{day}'.format(year=date_end.year, month=date_end.month, day=date_end.day)]
        else:
            return ['1000-01-01', '3000-01-01']

def get_daterange(year, month):
    u"""
    Возвращает строковое представление дат для выгрузки
    :return daterange :type list :var ['2019-03-01', '2019-03-31']"""
    month_endswith = { '01' : '01-31',
                       '02' : '02-28',
                       '03' : '03-31',
                       '04' : '04-30',
                       '05' : '05-31',
                       '06' : '06-30',
                       '07' : '07-31',
                       '08' : '08-31',
                       '09' : '09-30',
                       '10' : '10-31',
                       '11' : '11-30',
                       '12' : '12-31'}
    if is_leap_year(year):
        month_endswith['02'] = '02-29'
    if len(str(month)) == 1:
        month = str(0) + str(month)
    return [str(year) + '-' + str(month) + '-01', str(year) + '-' + month_endswith[month]]


def is_leap_year(year):
    year = int(year)
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False