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

def get_smo_length(data):
    smo_column_length = {}
    for smo, mo_dict in data.items():
        smo_column_length[smo] = len(list(mo_dict))
    return smo_column_length

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
        if args[0] == 'd_18_60' or args[0] == 'h_18_60' :
            date_begin = timezone.datetime.now() + relativedelta.relativedelta(years=-60, months=-11, days=-31)
            date_end = timezone.datetime.now() + relativedelta.relativedelta(years=-18)
            return ['{year}-{month}-{day}'.format(year=date_begin.year, month=date_begin.month, day=date_begin.day),
                    '{year}-{month}-{day}'.format(year=date_end.year, month=date_end.month, day=date_end.day)]
        elif args[0] == 'd_61' or args[0] == 'h_61':
            date_begin = timezone.now() + relativedelta.relativedelta(years=-170)
            date_end = timezone.now() + relativedelta.relativedelta(years=-61)
            return ['{year}-{month}-{day}'.format(year=date_begin.year, month=date_begin.month, day=date_begin.day),
                    '{year}-{month}-{day}'.format(year=date_end.year, month=date_end.month, day=date_end.day)]
        elif args[0] =='d_1_18':
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

def arabic_to_roman(arabic):

    if type(arabic) == str:
        arabic = int(arabic)
    start = arabic

    # print "arabic", arabic

    m = (arabic / 1000)
    arabic = arabic - (m * 1000)
    varm = ""
    count = 0
    while (count < m):
        varm = "M" + varm
        count = count + 1

    # print "varm", varm, "arabic", arabic, m

    d = (arabic / 500)
    arabic = arabic - (d * 500)
    vard = ""
    count = 0
    while (count < d):
        vard = "D" + vard
        count = count + 1

    # print "vard", vard, "arabic", arabic, d

    c = (arabic / 100)
    arabic = arabic - (c * 100)
    varc = ""
    count = 0
    while (count < c):
        varc = "C" + varc
        count = count + 1

    # print "varc", varm, "arabic", arabic, c

    l = (arabic / 50)
    arabic = arabic - (l * 50)
    varl = ""
    count = 0
    while (count < l):
        varl = "L" + varl
        count = count + 1

    # print "varl", varl, "arabic", arabic, l

    x = (arabic / 10)
    arabic = arabic - (x * 10)
    varx = ""
    count = 0
    while (count < x):
        varx = "X" + varx
        count = count + 1

    # print "varx", varx, "arabic", arabic, x

    v = (arabic / 5)
    arabic = arabic - (v * 5)
    varv = ""
    count = 0
    while (count < v):
        varv = "V" + varv
        count = count + 1

    # print "varv", varv, "arabic", arabic, v

    i = (arabic / 1)
    arabic = arabic - (i * 1)
    vari = ""
    count = 0
    while (count < i):
        vari = "I" + vari
        count = count + 1

    # print "vari", vari, "arabic", arabic, i

    # Reformat to take account of number 900s & 400s in arabic number
    if c == 4 and d == 1:  # =900
        vard = ""
        varc = "CM"
    elif c == 4 and d == 0:  # =400
        vard = ""
        varc = "CD"
    else:
        varc = varc
    # Reformat to take account of number 90s & 40s in arabic number
    if x == 4 and l == 1:  # =90
        varl = ""
        varx = "XC"
    elif x == 4 and l == 0:  # =40
        varl = ""
        varx = "XL"
    else:
        varx = varx
    # Reformat to take account of number 9s & 4s in arabic number
    if i == 4 and v == 1:  # =9
        vari = ""
        varv = "IX"
    elif i == 4 and v == 0:  # =4
        vari = "IV"
    else:
        varv = varv

    roman = (varm + vard + varc + varl + varx + varv + vari)
    return roman

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

def get_daterange_prev_period(daterange, prev_month=None, prev_year=None):
    if prev_month:
        d1 = timezone.datetime.strptime(daterange[0], '%Y-%m-%d') + relativedelta.relativedelta(months=-1)
        d2 = timezone.datetime.strptime(daterange[1], '%Y-%m-%d') + relativedelta.relativedelta(months=-1)
        daterange = ['{year}-{month}-{day}'.format(year=d1.year, month=correct_month(d1.month), day=correct_day(d1.day)),
                     '{year}-{month}-{day}'.format(year=d2.year, month=correct_month(d2.month), day=correct_day(d2.day))]
    if prev_year:
        d1 = timezone.datetime.strptime(daterange[0], '%Y-%m-%d') + relativedelta.relativedelta(years=-1)
        d2 = timezone.datetime.strptime(daterange[1], '%Y-%m-%d') + relativedelta.relativedelta(years=-1)
        daterange = ['{year}-{month}-{day}'.format(year=d1.year, month=correct_month(d1.month), day=correct_day(d1.day)),
                     '{year}-{month}-{day}'.format(year=d2.year, month=correct_month(d2.month), day=correct_day(d2.day))]
    return daterange

def correct_month(month):
    if len(str(month)) == 1:
        month = '0' + str(month)
    return month
def correct_day(day):
    if len(str(day)) == 1:
        day = '0' + str(day)
    return day

def get_date_to_show(year, month):
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
    returned_date = []
    if len(str(month)) == 1:
        month = '0' + str(month)
    daterange = get_daterange(year, month)
    daterange_month_ago = get_daterange_prev_period(daterange, prev_month=True)
    month_ago = daterange_month_ago[0].split('-')[1]
    second_year = daterange_month_ago[0].split('-')[0]
    year_ago = str(int(year) - 1)
    prefix = u'Выгрузка данных за'
    returned_date.append(u'{prefix} {month} {year} года/ {month_ago} {second_year} года.'.format(prefix=prefix,
                                                                                                 month=month_variables[month],
                                                                                                 year=year,
                                                                                                 month_ago=month_variables[month_ago],
                                                                                                 second_year=second_year))
    returned_date.append(u'{prefix} {month} {year} года/ {month} {year_ago} года.'.format(prefix=prefix,
                                                                                                 month=month_variables[month],
                                                                                                 year=year,
                                                                                                 year_ago=year_ago))
    return returned_date


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

def set_mkb_to_finder(mkb):
    if len(mkb) > 3:
        pass
    else:
        slice_mkb = mkb[1:]
        head_mkb = mkb[0]
        next_ = int(slice_mkb) + 1
        if next_ == 100:
            suff = 'AA'
        else:
            suff = str(next_)
            if len(suff) == 1:
                suff = '0' + suff
        mkb = head_mkb + suff
    return mkb

