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

def get_data_to_result_header(month, year):
    month_variables = {'01': 'Январь',
                       '02': 'Февраль',
                       '03': 'Март',
                       '04': 'Апрель',
                       '05': 'Май',
                       '06': 'Июнь',
                       '07': 'Июль',
                       '08': 'Август',
                       '09': 'Сентябрь',
                       '10': 'Октябрь',
                       '11': 'Ноябрь',
                       '12': 'Декабрь'}
    if len(str(month)) == 1:
        month = str(0) + str(month)
    else:
        month = str(month)
    return month_variables.get(month, '') + u' ' + str(year)


roman_number={'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

def repetitive_number(string, count, qty):
    repetitive_counter = 0
    if count+qty < len(string):
        while repetitive_counter < qty+1:
            if string[count + repetitive_counter] == string[count]:
                repetitive_counter+=1
            else:
                break
    if repetitive_counter == qty+1:
        return None
    else:
        return True

def roman_to_arabic(string):
    u'''

    :param string:
    :return: :type: str
    '''
    count = 0
    total = 0

    if type(string) is not str:
        return None

    if not string:
        return None

    while count < len(string):
        if string[count] not in roman_number:
            return None
        elif string[count] == 'I':
            if count + 1 < len(string) and string[count + 1] == 'X':
                total += roman_number['X'] - roman_number['I']
                count += 1
            elif count + 1 < len(string) and string[count + 1] == 'V':
                total += roman_number['V'] - roman_number['I']
                count += 1
                if count + 1 < len(string):
                    return None
            elif count + 1 < len(string) and string[count + 1] in ['M', 'D', 'C', 'L']:
                return None
            else:
                total += roman_number['I']
                if not repetitive_number(string, count, 3):
                    return None
        elif string[count] == 'V':
            total += roman_number[string[count]]
            if count + 1 < len(string) and string[count + 1] in ['M', 'D', 'C', 'L', 'X']:
                return None
            if not repetitive_number(string, count, 1):
                return None
        elif string[count] == 'X':
            if count + 1 < len(string) and string[count + 1] == 'L':
                total += roman_number['L'] - roman_number['X']
                count += 1
            elif count + 1 < len(string) and string[count + 1] == 'C':
                total += roman_number['C'] - roman_number['X']
                count += 1
            elif count + 1 < len(string) and string[count + 1] in ['M', 'D']:
                return None
            else:
                total += roman_number['X']
                if not repetitive_number(string, count, 3):
                    return None
        elif string[count] == 'L':
            total += roman_number[string[count]]
            if count + 1 < len(string) and string[count + 1] in ['M', 'D', 'C']:
                return None
            if not repetitive_number(string, count, 1):
                return None
        elif string[count] == 'C':
            if count + 1 < len(string) and string[count + 1] == 'D':
                total += roman_number['D'] - roman_number['C']
                count += 1
            elif count + 1 < len(string) and string[count + 1] == 'M':
                total += roman_number['M'] - roman_number['C']
                count += 1
            elif count + 1 < len(string) and string[count + 1] in ['M']:
                return None
            else:
                total += roman_number['C']
                if not repetitive_number(string, count, 3):
                    return None
        elif string[count] == 'D':
            total += roman_number[string[count]]
            if count + 1 < len(string) and string[count + 1] in ['M']:
                return None
            if not repetitive_number(string, count, 1):
                return None
        elif string[count] == 'M':
            total += roman_number[string[count]]

        count += 1

    return total

def arabic_to_str(number):
    number = str(number)
    if len(number) == 1:
        return '0'+number
    else:
        return number

MKB_CLASS_RANGE = {
    '01'    : 'A00-B99',
    '02'    : 'C00-D48',
    '03'    : 'D50-D99',
    '04'    : 'E00-E99',
    '05'    : 'F00-F99',
    '06'    : 'G00-G99',
    '07'    : 'H00-H59',
    '08'    : 'H60-H95',
    '09'    : 'I00-I99',
    '10'    : 'J00-J99',
    '11'    : 'K00-K93',
    '12'    : 'L00-L99',
    '13'    : 'M00-M99',
    '14'    : 'N00-N99',
    '15'    : 'O00-O99',
    '16'    : 'P00-P96',
    '17'    : 'Q00-Q99',
    '18'    : 'R00-R99',
    '19'    : 'S00-T98',
    '20'    : 'V01-Y98',
    '21'    : 'Z00-Z99',
    '22'    : 'U00-U85'
}

MKB_CLASS_RANGE_ROMAN = {
    'I'    : 'A00-B99',
    'II'   : 'C00-D48',
    'III'  : 'D50-D99',
    'IV'   : 'E00-E99',
    'V'    : 'F00-F99',
    'VI'   : 'G00-G99',
    'VII'  : 'H00-H59',
    'VIII' : 'H60-H95',
    'IX'   : 'I00-I99',
    'X'    : 'J00-J99',
    'XI'   : 'K00-K93',
    'XII'  : 'L00-L99',
    'XIII' : 'M00-M99',
    'XIV'  : 'N00-N99',
    'XV'   : 'O00-O99',
    'XVI'  : 'P00-P96',
    'XVII' : 'Q00-Q99',
    'XVIII': 'R00-R99',
    'XIX'  : 'S00-T98',
    'XX'   : 'V01-Y98',
    'XXI'  : 'Z00-Z99',
    'XXII' : 'U00-U85'
}