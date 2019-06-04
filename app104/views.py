from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.conf import settings
from .models import SLS, Nosologies, Lpu_names, Patients, Z_SLS
from django.db.models import Count,Q
from django.utils import timezone
from dateutil import relativedelta


global _data, _data_coord_death, _lpu_names
_data = []
_data_coord_death = {}
_lpu_names = {}

def load_data(request):
    if not _data:
        daterange = ["2019-03-01", "2019-03-31"]
        nosologies = Nosologies.objects.all()
        lpu_list = []
        lpus = {1: 47007406,
                2: 470067,
                3: 470003,
                4: 470006}

        for k, v in lpus.items():
            if len(str(v)) > 7:
                lpus[k] = str(v)[:6]
            else:
                lpus[k] = str(v)
            try:
                _lpu_names[lpus[k]] = Lpu_names.objects.using('dictadmin').filter(lpu_id=int(lpus[k])).values_list('name_short',flat=True)[0]
            except:
                _lpu_names[lpus[k]] = lpus[k]
        for k, v in lpus.items():
            lpu_list.append(SLS.objects.select_related('caseZid').filter(dateBeg__range=daterange, lpuId__startswith=v).annotate(ds1count=Count(SLS.mkbExtra)))
            lpu_list.append(SLS.objects.select_related('caseZid').filter(dateBeg__range=daterange, lpuId__startswith=v, caseZid__stat_or_amb__in=[1,2]).annotate(
                ds1count=Count(SLS.mkbExtra)))
            lpu_list.append(
                SLS.objects.select_related('caseZid').filter(dateBeg__range=daterange).filter(lpuId__startswith=v, caseZid__stat_or_amb__in=3).annotate(
                    ds1count=Count(SLS.mkbExtra)))
        row = [0 for j in range(len(lpu_list) + 5)]
        for i, n in enumerate(nosologies):
            _data.append([0 for j in range(len(lpu_list) + 5)])
            _data[i][0] = n.number
            _data[i][1] = n.name
            for num, lpu1 in enumerate(lpu_list):
                for lpu in lpu1:
                    if (n.mkbFirst <= lpu.mkbExtra) and (n.mkbLast >= lpu.mkbExtra):
                        _data[i][num + 2] += lpu.ds1count
                        if num % 3 == 0:
                            _data[i][len(row) - 3] += lpu.ds1count
                        elif num % 3 == 1:
                            _data[i][len(row) - 2] += lpu.ds1count
                        else:
                            _data[i][len(row) - 1] += lpu.ds1count

    return render(request, 'base.html')

def base(request):
    return render(request, 'base.html')


def index(request):
    data, lpus = get_data(request)
    return render(request, 'index.html', {'data' : data,
                                          'lpus' : lpus
                                          })

def mo_views(request):
    data, lpus = get_data(request)


    return render(request, 'mo_views.html', {'data': data,
                                          'lpus': lpus
                                          })

def mo_views_table(request):
    u"""
    Данная вьюха выглядит максимально готовой( тут нужна только оптимизация разделения случаев на амбулаторные и стационарные)
    """
    data, lpus = get_data(request)
    if _lpu_names:
        return render(request, 'mo_views_table.html', {'data' : data,
                                                   'lpus' : _lpu_names})
    else:
        return render(request, 'mo_views_table.html', {'data': data,
                                                       'lpus': lpus})

def mo_views_ctrl_tbl(request):
    u"""
    Тут необходимо накладывать данные из таблицы выше
    и сравнивать их с ожидаемыми  (изменять заливку ячейки в случае различий)
    :param request:
    :return:
    """
    data, lpus = get_data(request)
    if _lpu_names:
        return render(request, 'mo_views_control_table.html', {'data' : data,
                                                           'lpus' : _lpu_names})
    else:
        return render(request, 'mo_views_table.html', {'data': data,
                                                       'lpus': lpus})
def documents_base(request):
    return render(request, 'documents_base.html')

def documents_all(request):
    return render(request, 'documents_all.html')

def documents_new(request):
    return render(request, 'documents_new.html')

def coordination(request):
    data, lpus = get_data(request)
    if _lpu_names:
        return render(request, 'mo_views_control_table.html', {'data' : data,
                                                           'lpus' : _lpu_names})
    else:
        return render(request, 'mo_views_table.html', {'data': data,
                                                       'lpus': lpus})

def coord_illness(request):
    u"""
    Что будет - таблица отчета по заболеваемости
    :param request:
    :return:
    """

    return render(request,'coordination_illness.html')

def coord_death(request):
    u"""
    Что будет - таблица отчета по смертности
    :param request:
    :return:
    """
    return  render(request, 'coordination_death.html')


def onload(request):
    return render(request, 'index.html')

def get_data(request):
    u"""
    Универсальный метод подгрузки данных в формы.
    На тестовом образце таким простым образом реализовано кэширование(хранятся данные в списке
    _data
    :return: данные + список лпу( на данный момент нет списка организаций Лен. Области)
    """
    lpus = {1: 47007406,
            2: 470067,
            3: 470003,
            4: 470006}
    for k, v in lpus.items():
        if len(str(v)) > 7:
            lpus[k] = str(v)[:6]
        else:
            lpus[k] = str(v)
    if _data:
        return _data, lpus
    else:
        load_data(request)
    return _data, lpus

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

def data_for_coord_death(request, *args):
    u"""
    При Включении сервиса подгружает данные для
    построения форм отчетности по смертности
    :param request:
    :param args:
    :return:
    """
    death_list = [105, 106, 205, 206, 313, 405, 406, 411]
    daterange = ['2019-03-01', '2019-03-31']
    nosologies = Nosologies.objects.all()
    cases = SLS.objects.select_related('caseZid__zap_id').filter(dateBeg__range=daterange,
                                                                 caseZid__result__in=death_list,
                                                                 caseZid__zap_id__date_birth__range=calculate_date(args),
                                                                 caseZid__isnull=False)
    amb = cases.filter(caseZid__stat_or_amb=3)
    stat = cases.filter(caseZid__stat_or_amb__in=[1,2])
    stat_zam = cases.filter(caseZid__stat_or_amb__isnull=True)
    skor_mp = cases.filter(caseZid__stat_or_amb=4).exclude(unit__startswith=SLS.lpuId)

    if args and not check_cache_coord_death(args, len(nosologies) + 1):
        sum_amb = 0
        sum_stat = 0
        sum_stat_zam = 0
        sum_skor_mp = 0
        for number, _obj in enumerate(nosologies):
            row = [0 for j in range(7)]
            row[0] = _obj.number
            row[1] = _obj.name
            row[2] = (_obj.mkbFirst + ' - ' + _obj.mkbLast) if _obj.mkbFirst != _obj.mkbLast else _obj.mkbFirst
            count_amb = 0
            for sl in amb:
                if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                    count_amb += 1
            count_stat = 0
            for sl in stat:
                if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >=sl.mkbExtra:
                    count_stat+=1
            count_stat_zam = 0
            for sl in stat_zam:
                if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                    count_stat_zam +=1
            count_skor_mp = 0
            for sl in skor_mp:
                if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                    count_skor_mp += 1
            row[3] = count_amb
            row[4] = count_stat
            row[5] = count_stat_zam
            row[6] = count_skor_mp
            if _data_coord_death.get(args[0], None):
                _data_coord_death[args[0]].append(row)
            else:
                _data_coord_death[args[0]] = [row]
            sum_amb += count_amb
            sum_stat += count_stat
            sum_stat_zam += count_stat_zam
            sum_skor_mp += count_skor_mp
        # последняя строка
        row = [0 for j in range(7)]
        row[0] = '.....'
        row[1] = 'Итого:'
        row[2] = '.....'
        row[3] = sum_amb
        row[4] = sum_stat
        row[5] = sum_stat_zam
        row[6] = sum_skor_mp
        if _data_coord_death.get(args[0], None):
            _data_coord_death[args[0]].append(row)
        else:
            _data_coord_death[args[0]] = [row]




def check_cache_coord_death(args, count):
    u"""
    проверяет наличие в кэше необходимых для построения таблиц данных,
    чтобы не запрашивать из базы
    :param args:
    :return: bool
    """

    if args and (len(args) > 0) and _data_coord_death.get(args[0], None) and count == len(_data_coord_death[args[0]]):
        return True
    else:
        return False


def coord_death_urls(request, *args):
    u"""
    В зависимости от полученного запроса генерирует таблицу
    :param request:
    :return:
    """
    data_for_coord_death(request, *args)
    if args and len(args) > 0:
        return render(request, 'coordination_death.html', {'data' : _data_coord_death[args[0]]})



