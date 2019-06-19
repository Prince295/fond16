import pandas as pd
from django_pandas.managers import DataFrameManager
from django_pandas.io import read_frame

from django.shortcuts import render, resolve_url
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.conf import settings
from django.db.models import Count,Q
from django.db.models.functions import Length
from django.utils import timezone
from dateutil import relativedelta
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from .views_utils import copy_data, get_daterange, get_column, is_leap_year, calculate_date
from .models import SLS, Nosologies, Lpu_names, Patients, Z_SLS, Smo_names


global _data, _data_coord_death, _lpu_names, _data_coord_illness, _data_coord_illness_prev_year, data_for_illness_prev_month, _names

_data = []
_data_coord_death = {}
_lpu_names = {}
_data_coord_illness = {}
_data_coord_illness_prev_year = {} #нужен для построения сравнительного отчета\
_data_coord_illness_result = {}
_data_coord_illness_prev_month = {} #нужен для построения сравнительного отчета ( дальше будет структура, сохраняющая более цельно)
_names = {}  #присваивает названия лпшушкам и смошкам в отчете

def authentificate_func(request):
    u"""
    Аутентифицирует и авторизует пользователя
    :param request: пост запрос с именем пользователя и паролем
    :return: HttpResponse (успех или ошибка)
    """


    redirect_field_name = REDIRECT_FIELD_NAME
    redirect_to = request.POST.get(
            redirect_field_name,
            request.GET.get(redirect_field_name, '')
        )
    redirect_to = redirect_to or resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to=redirect_to)
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

        return render(request, 'coordination_illness.html', {'user' : user})
    else:
        return render(request, 'coordination_illness.html')

def logout_func(request):
    logout(request)
    return render(request, 'coordination_illness.html')


def load_data(request):
    u"""
    Выгрузка всех случаев в сводную таблицу
    ( на тестовой базе размер таблицы около 100 мб, что позволяет выгружать все данные,
    в дальнейшем будет иметь смысл догружать данные, а не выгружать их заново,
    к сожалению, на базе Фонда ЛО не хранится информация  о createDateTime и ModifyDateTime случаев и пациентов

    :param request:
    :return: Возвращает на 107 форму
    """

    d_reader = DataReader()
    all_smo = d_reader.load_model_smo_names()
    all_mo = d_reader.load_model_mo_names()
    df_blood = d_reader.get_all_cases()
    df_blood.to_csv('data/all_cases')
    return render(request, 'coordination_illness.html', {'smo_data' : all_smo,
                                                         'mo_data'  : all_mo})

def base(request):
    all_smo = Smo_names.objects.using('dictadmin').all();
    all_mo = Lpu_names.objects.using('dictadmin').all();
    return render(request, 'coordination_illness.html', {'smo_data' : all_smo,
                                                         'mo_data'  : all_mo  })


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

@login_required(login_url='/fond16/login/')
def documents_all(request):
    return render(request, 'documents_all.html')

@login_required(login_url='/fond16/login/')
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

def success_auth(request):
    return render(request, 'coordination_illness.html')

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
    nosologies = Nosologies.objects.all().order_by('id')
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
        row[0] = '..'
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


def data_for_illness(request, prev_month, prev_year, mo_list, smo_list, daterange,  *args):
    u"""
    Данные по заболеваемости за выбранный месяц,
    также данные за прошлый месяц и данные за тот же месяц в прошлом году
    :argument nosologies - таблица всех нозологий (заведена вручную)
    :argument cases - данные из таблицы TFOMS_DATA_31.SLS, объединенной по внешнему ключу с TFOMS_DATA_31.Z_SLS
    и TFOMS_DATA_31.PACIENTS -данные сгруппированы по СМО
    :argument MO -
    :argument stat_or_amb 1 - Стационар,
                        2 - Дневной стационар
                        3 - Поликлиника,
                        4 - Скорая помощь
    :argument
    :param request:
    :param args:
    :param _data_coord_illness - результирующий кэш с данными, из которого будут подтягиваться цифры по отчетам:
    _data_coord_illness = {
 'adult' : {'smo1' : {'mo1' : {'nos1' : {'amb'  : 12,
                                         'stat' : 14,
                                         'cmp'  : 10},
                               'nos2' : {'amb'  : 3,
                                         'stat' : 4,
                                         'cmp'  : 2}},
                      'mo2' : {'nos1' : {'amb'  : 12,
                                         'stat' : 1,
                                         'cmp'  : 10},
                               'nos2' : {'amb'  : 3,
                                         'stat' : 4,
                                         'cmp'  : 2}},
                      'mo3' : {'nos1' : {'amb'  : 2,
                                         'stat' : 14,
                                         'cmp'  : 20},
                               'nos2' : {'amb'  : 3,
                                         'stat' : 4,
                                         'cmp'  : 2}}},
            'smo2' : {'mo1' : {'nos1' : {'amb'  : 12,
                                         'stat' : 4,
                                         'cmp'  : 18},
                               'nos2' : {'amb'  : 30,
                                         'stat' : 45,
                                         'cmp'  : 27}}}},
 'child' : {'smo1' : {'mo1' : {'nos1' : {'amb'  : 12,
                                         'stat' : 14,
                                         'cmp'  : 10},
                               'nos2' : {'amb'  : 3,
                                         'stat' : 4,
                                         'cmp'  : 2}},
                      'mo2' : {'nos1' : {'amb'  : 12,
                                         'stat' : 1,
                                         'cmp'  : 10},
                               'nos2' : {'amb'  : 3,
                                         'stat' : 4,
                                         'cmp'  : 2}},
                      'mo3' : {'nos1' : {'amb'  : 2,
                                         'stat' : 14,
                                         'cmp'  : 20},
                               'nos2' : {'amb'  : 3,
                                         'stat' : 4,
                                         'cmp'  : 2}}},
            'smo2' : {'mo1' : {'nos1' : {'amb'  : 12,
                                         'stat' : 4,
                                         'cmp'  : 18},
                               'nos2' : {'amb'  : 30,
                                         'stat' : 45,
                                         'cmp'  : 27}}}},
                      }
    на боевом сервере данная структура будет подгятиваться по всем смо и всем мо. на данный момент структура динамически
    заполняется при выборе фильтра отчетности для каждого из фильтров. В тестовой версии список СМО и МО сокращен.
    Во всяком случае до ввода фильтра про МО и СМО и подтягивания данных в соответствии со значениями этого фильтра
    :return: записи в глобальной переменной _data_for_illness
    """
    if prev_month:
        d1 = timezone.datetime.strptime(daterange[0], '%Y-%m-%d') + relativedelta.relativedelta(months=-1)
        d2 = timezone.datetime.strptime(daterange[1], '%Y-%m-%d') + relativedelta.relativedelta(months=-1)
        daterange = ['{year}-{month}-{day}'.format(year=d1.year, month=d1.month, day=d1.day),
                     '{year}-{month}-{day}'.format(year=d2.year, month=d2.month, day=d2.day)]
    if prev_year:
        d1 = timezone.datetime.strptime(daterange[0], '%Y-%m-%d') + relativedelta.relativedelta(years=-1)
        d2 = timezone.datetime.strptime(daterange[1], '%Y-%m-%d') + relativedelta.relativedelta(years=-1)
        daterange = ['{year}-{month}-{day}'.format(year=d1.year, month=d1.month, day=d1.day),
                     '{year}-{month}-{day}'.format(year=d2.year, month=d2.month, day=d2.day)]


    for smo in smo_list:
        _names[smo] = Smo_names.objects.using('dictadmin').filter(smo_id=int(smo)).values_list('short_name',flat=True)
        if len(_names[smo] ) > 0 :
            _names[smo] = _names[smo][0]
        else:
            _names[smo] = u'Неизвестно'
    for mo in mo_list:
        _names[str(mo)] = Lpu_names.objects.using('dictadmin').filter(lpu_id=int(mo)).values_list('name_short',flat=True)[0]
    nosologies = Nosologies.objects.all().order_by('id')
    cases = SLS.objects.select_related('caseZid__zap_id').filter(caseZid__dateBeg__range=daterange,
                                                                 caseZid__zap_id__date_birth__range=calculate_date(args))

    if args and not check_cache_coord_illness_age(_data_coord_illness, args):
        _data_coord_illness[args[0]] = {}
    for smo in smo_list:
        if not check_cache_coord_illness_smo(_data_coord_illness, args, smo_list):
            _data_coord_illness[args[0]][smo] = {}
        smo_filter = cases.filter(caseZid__zap_id__smo_id=smo)
        for mo in mo_list:
            if not check_cache_coord_illness_mo(_data_coord_illness, args, mo_list, smo):
                mo_filter = smo_filter.filter(caseZid__lpu=mo)
                amb = mo_filter.filter(caseZid__stat_or_amb=3)
                stat = mo_filter.filter(caseZid__stat_or_amb__in=[1, 2])
                stat_zam = mo_filter.filter(caseZid__stat_or_amb__isnull=True)
                skor_mp = mo_filter.filter(caseZid__stat_or_amb=4)
                sum_amb = 0
                sum_stat = 0
                sum_stat_zam = 0
                sum_skor_mp = 0
                for number, _obj in enumerate(nosologies):
                    row = [0 for j in range(7)]
                    row[0] = _obj.number
                    row[1] = _obj.name
                    row[2] = (
                                _obj.mkbFirst + ' - ' + _obj.mkbLast) if _obj.mkbFirst != _obj.mkbLast else _obj.mkbFirst
                    count_amb = 0
                    for sl in amb:
                        if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                            count_amb += 1
                    count_stat = 0
                    for sl in stat:
                        if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                            count_stat += 1
                    count_stat_zam = 0
                    for sl in stat_zam:
                        if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                            count_stat_zam += 1
                    count_skor_mp = 0
                    for sl in skor_mp:
                        if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                            count_skor_mp += 1
                    row[3] = count_amb
                    row[4] = count_stat
                    row[5] = count_stat_zam
                    row[6] = count_skor_mp
                    if _data_coord_illness[args[0]][smo].get(mo, None):
                        _data_coord_illness[args[0]][smo][mo].append(row)
                    else:
                        _data_coord_illness[args[0]][smo][mo] = [row]
                    sum_amb += count_amb
                    sum_stat += count_stat
                    sum_stat_zam += count_stat_zam
                    sum_skor_mp += count_skor_mp
                # последняя строка
                row = [0 for j in range(7)]
                row[0] = '..'
                row[1] = 'Итого:'
                row[2] = '.....'
                row[3] = sum_amb
                row[4] = sum_stat
                row[5] = sum_stat_zam
                row[6] = sum_skor_mp
                if _data_coord_illness[args[0]][smo].get(mo, None):
                    _data_coord_illness[args[0]][smo][mo].append(row)
                else:
                    _data_coord_illness[args[0]][smo][mo] = [row]


def data_for_illness_prev(request, prev_month, prev_year, mo_list, smo_list, daterange, *args):
    u"""
    TODO: Так делать нехорошо. Поменяю структуру
    Дубль функции для извлечения данных по заболеваниям ( нужен, чтобы не запутаться в глобальных словарях)
    :return: записи в глобальной переменной _data_for_illness_prev_month or _data_for_illness_prev_year
    """


    if prev_month:
        d1 = timezone.datetime.strptime(daterange[0], '%Y-%m-%d') + relativedelta.relativedelta(months=-1)
        d2 = timezone.datetime.strptime(daterange[1], '%Y-%m-%d') + relativedelta.relativedelta(months=-1)
        daterange = ['{year}-{month}-{day}'.format(year=d1.year, month=d1.month, day=d1.day),
                     '{year}-{month}-{day}'.format(year=d2.year, month=d2.month, day=d2.day)]
    if prev_year:
        d1 = timezone.datetime.strptime(daterange[0], '%Y-%m-%d') + relativedelta.relativedelta(years=-1)
        d2 = timezone.datetime.strptime(daterange[1], '%Y-%m-%d') + relativedelta.relativedelta(years=-1)
        daterange = ['{year}-{month}-{day}'.format(year=d1.year, month=d1.month, day=d1.day),
                     '{year}-{month}-{day}'.format(year=d2.year, month=d2.month, day=d2.day)]

    nosologies = Nosologies.objects.all().order_by('id')
    cases = SLS.objects.select_related('caseZid__zap_id').filter(caseZid__dateBeg__range=daterange,
                                                                 caseZid__zap_id__date_birth__range=calculate_date(
                                                                     args))
    if args and not check_cache_coord_illness_age(_data_coord_illness_prev_year, args):
        _data_coord_illness_prev_year[args[0]] = {}
    for smo in smo_list:
        if not check_cache_coord_illness_smo(_data_coord_illness_prev_year, args, smo_list):
            _data_coord_illness_prev_year[args[0]][smo] = {}
        smo_filter = cases.filter(caseZid__zap_id__smo_id=smo)
        for mo in mo_list:
            if not check_cache_coord_illness_mo(_data_coord_illness_prev_year, args, mo_list, smo):
                mo_filter = smo_filter.filter(caseZid__lpu=mo)
                amb = mo_filter.filter(caseZid__stat_or_amb=3)
                stat = mo_filter.filter(caseZid__stat_or_amb__in=[1, 2])
                stat_zam = mo_filter.filter(caseZid__stat_or_amb__isnull=True)
                skor_mp = mo_filter.filter(caseZid__stat_or_amb=4)
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
                        if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                            count_stat += 1
                    count_stat_zam = 0
                    for sl in stat_zam:
                        if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                            count_stat_zam += 1
                    count_skor_mp = 0
                    for sl in skor_mp:
                        if _obj.mkbFirst <= sl.mkbExtra and _obj.mkbLast >= sl.mkbExtra:
                            count_skor_mp += 1
                    row[3] = count_amb
                    row[4] = count_stat
                    row[5] = count_stat_zam
                    row[6] = count_skor_mp
                    if _data_coord_illness_prev_year[args[0]][smo].get(mo, None):
                        _data_coord_illness_prev_year[args[0]][smo][mo].append(row)
                    else:
                        _data_coord_illness_prev_year[args[0]][smo][mo] = [row]
                    sum_amb += count_amb
                    sum_stat += count_stat
                    sum_stat_zam += count_stat_zam
                    sum_skor_mp += count_skor_mp
                # последняя строка
                row = [0 for j in range(7)]
                row[0] = '..'
                row[1] = 'Итого:'
                row[2] = '.....'
                row[3] = sum_amb
                row[4] = sum_stat
                row[5] = sum_stat_zam
                row[6] = sum_skor_mp
                if _data_coord_illness_prev_year[args[0]][smo].get(mo, None):
                    _data_coord_illness_prev_year[args[0]][smo][mo].append(row)
                else:
                    _data_coord_illness_prev_year[args[0]][smo][mo] = [row]




def check_cache_coord_death(args, count):
    u"""
    проверяет наличие в кэше необходимых для построения таблиц данных,
    чтобы не запрашивать из базы
    :param args: аргумент get-запроса, показывающий хвост ссылки :type string:
    :param count: количество строк :type int
    :return: :type bool
    """

    if args and (len(args) > 0) and _data_coord_death.get(args[0], None) and count == len(_data_coord_death[args[0]]):
        return True
    else:
        return False

def check_cache_coord_illness_age(_dict, args):
    u"""
    Проверяет наличие в кэше необходимых данных для построения таблиц,
    чтобы не тянуть из базы ( на боевом сервере из результирующей таблицы)
    :param args: аргумент get-запроса, показывающий хвост ссылки :type string

    :param count: количество столбцов :type int
    :return: :type bool
    """

    if args and (len(args) > 0) and _dict.get(args[0], None):
        return True
    else:
        return False

def check_cache_coord_illness_smo(_dict, args, smo_list):
    u"""
        Проверяет наличие в кэше необходимых данных для построения таблиц,
        чтобы не тянуть из базы ( на боевом сервере из результирующей таблицы)
        :param args: аргумент get-запроса, показывающий хвост ссылки :type string
        :param smo_list: список страховых компаний :type list
        :param count: количество столбцов :type int
        :return: :type bool
        """
    if not check_cache_coord_illness_age(_dict, args):
        for smo in smo_list:
            if not _dict[args[0]].get(smo, None):
                return False
    else:
        return False
    return True

def check_cache_coord_illness_mo(_dict, args, mo_list, smo):
    u"""
        Проверяет наличие в кэше необходимых данных для построения таблиц,
        чтобы не тянуть из базы ( на боевом сервере из результирующей таблицы)
        :param args: аргумент get-запроса, показывающий хвост ссылки :type String
        :param mo_list: список больниц :type list
        :param smo: id страховой компании :type string
        :param count: количество столбцов :type int
        :return: :type bool
        """
    for mo in mo_list:
        if not _dict[args[0]][smo].get(mo, None):
            return False
    return True






def coord_illness_urls(request, *args):
    u"""
        В зависимости от полученного запроса генерирует таблицу
        :param request:
        :return:
        """
    all_smo = Smo_names.objects.using('dictadmin').all();
    all_mo = Lpu_names.objects.using('dictadmin').all();
    selected_mo = request.GET.get('selected_mo', None)
    selected_smo = request.GET.get('selected_smo', None)
    selected_year_1 = request.GET.get('selected_year_1', None)
    selected_month_1 = request.GET.get('selected_month_1', None)
    selected_year_2 = request.GET.get('selected_year_2', None)
    selected_month_2 = request.GET.get('selected_month_2', None)
    if selected_mo and selected_smo:
        selected_mo = selected_mo.split(',')
        selected_smo = selected_smo.split(',')
        data_for_illness(request,None, None, selected_mo, selected_smo, get_daterange(selected_year_1, selected_month_1), args[0])
        data_for_illness_prev(request, True, None, selected_mo, selected_smo, get_daterange(selected_year_2, selected_month_2), args[0])
        len_smo = {}
        calculated_data = return_data_illness(request, args, selected_smo, selected_mo)
        if args and len(args) > 0:
            for smo_name, smo_val in _data_coord_illness[args[0]].items():
                for mo_name, mo_val in smo_val.items():
                    len_mo = len(mo_val) + 1
                len_smo = len(_data_coord_illness[args[0]][smo_name].keys()) * len_mo
            return render(request, 'coordination_illness.html', {'data' : calculated_data[args[0]],
                                                                 'smo_list_len' : len_smo,
                                                                 'mo_list_len' : len_mo,
                                                                 'names_list' : _names,
                                                                 'smo_data' : all_smo,
                                                                 'mo_data' : all_mo})
    else:
        return render(request, 'coordination_illness.html', {'smo_data'  : all_smo,
                                                             'mo_data'   : all_mo,
                                                             'names_list': _names})

def return_data_illness(request, args, smo_list, mo_list):
    u"""
    Функция берет 2 словаря из глобальных данных,
    сравнивает значения в них - пересчитывает их в отдельный словарь, который и уходит в отчет
    :arg _data_coord_illness - данные по заболеваниям за отчетный месяц
    :arg _data_coord_illness_prev_year - данные по заболеваниям за отчетный месяц в предыдущем календарном году

    :return: data_for_print :type dict
    """

    data_for_print = {args[0]: {}}
    data_for_print[args[0]] = copy_data(data_for_print[args[0]], _data_coord_illness[args[0]], smo_list, mo_list)
    for smo, mo_dict in _data_coord_illness[args[0]].items():
        if str(smo) in smo_list:
            for mo, rows in mo_dict.items():
                if str(mo) in mo_list:
                    for j, row in enumerate(rows):
                        for i in range(3):
                            data_for_print[args[0]][smo][mo][j][i] = _data_coord_illness_prev_year[args[0]][smo][mo][j][i]
                        for i in range(3,7,1):
                            data_for_print[args[0]][smo][mo][j][i] = get_column(_data_coord_illness[args[0]][smo][mo][j][i], _data_coord_illness_prev_year[args[0]][smo][mo][j][i])
    return data_for_print



def coord_death_urls(request, *args):
    u"""
    В зависимости от полученного запроса генерирует таблицу
    :param request:
    :return:
    """
    data_for_coord_death(request, *args)
    if args and len(args) > 0:
        return render(request, 'coordination_death.html', {'data' : _data_coord_death[args[0]]})




class DataReader():
    u"""
    Класс для возврата DataFrame объектов
    с фильтрацией по основным нозологическим формам
    :return :type pd.DataFrame
    """
    def get_blood_illness(self):
        cases = SLS.objects.select_related('caseZid__zap_id') \
            .values('caseZid__zap_id__smo_id', 'caseZid__lpu', 'caseZid__stat_or_amb', 'mkbExtra', 'caseZid__dateBeg',
                    'caseZid__dateEnd', 'caseZid__result',
                    'caseZid__zap_id__date_birth') \
            .filter(mkbExtra__gte='I00', mkbExtra__lte='I99')
        return read_frame(cases)

    def get_newpat_illness(self):
        cases = SLS.objects.select_related('caseZid__zap_id') \
            .values('caseZid__zap_id__smo_id', 'caseZid__lpu', 'caseZid__stat_or_amb', 'mkbExtra', 'caseZid__dateBeg',
                    'caseZid__dateEnd', 'caseZid__result',
                    'caseZid__zap_id__date_birth') \
            .filter(mkbExtra__gte='C00', mkbExtra__lte='D48')
        return read_frame(cases)

    def get_neuron_netw_illness(self):
        cases = SLS.objects.select_related('caseZid__zap_id') \
            .values('caseZid__zap_id__smo_id', 'caseZid__lpu', 'caseZid__stat_or_amb', 'mkbExtra', 'caseZid__dateBeg',
                    'caseZid__dateEnd', 'caseZid__result',
                    'caseZid__zap_id__date_birth') \
            .filter(mkbExtra__gte='G00', mkbExtra__lte='G98')
        return read_frame(cases)

    def get_breath_illness(self):
        cases = SLS.objects.select_related('caseZid__zap_id') \
            .values('caseZid__zap_id__smo_id', 'caseZid__lpu', 'caseZid__stat_or_amb', 'mkbExtra', 'caseZid__dateBeg',
                    'caseZid__dateEnd', 'caseZid__result',
                    'caseZid__zap_id__date_birth') \
            .filter(mkbExtra__gte='J00', mkbExtra__lte='J99')
        return read_frame(cases)

    def get_digestion_illness(self):
        cases = SLS.objects.select_related('caseZid__zap_id') \
            .values('caseZid__zap_id__smo_id', 'caseZid__lpu', 'caseZid__stat_or_amb', 'mkbExtra', 'caseZid__dateBeg',
                    'caseZid__dateEnd', 'caseZid__result',
                    'caseZid__zap_id__date_birth') \
            .filter(mkbExtra__gte='K00', mkbExtra__lte='K93')
        return read_frame(cases)

    def get_all_cases(self):
        cases = SLS.objects.select_related('caseZid__zap_id') \
            .values('caseZid__zap_id__smo_id', 'caseZid__lpu',  'caseZid__stat_or_amb', 'mkbExtra', 'caseZid__dateBeg',
                    'caseZid__dateEnd', 'caseZid__result',
                            'caseZid__zap_id__date_birth')
        return read_frame(cases)

    def load_model_smo_names(self):
        return Smo_names.objects.using('dictadmin').all()

    def load_model_mo_names(self):
        return Lpu_names.objects.using('dictadmin').all()

    def get_nosologies(self):
        return Nosologies.objects.all().order_by('id')


class Coordination_illness_views():

    def __init__(self):
        self.dateMonth1 = None # type: int
        self.dateYear1 = None # type: int
        self.dateMonth2 = None # type: int
        self.dateYear2 = None # type: int
        self.selectedSmo = None # type: list
        self.selectedMo = None # type: list

        self.nosologies = None # type: django.QuerySet
        self.query = None # type: pandas.DataFrame
        self.query_copy = None #type: pandas.DataFrame

    def setup_Settings(self, params):

        self.dateMonth1 = params.get('selected_month_1', None)
        self.dateYear1 = params.get('selected_year_1', None)
        self.dateMonth2 = params.get('selected_month_2', None)
        self.dateYear2 = params.get('selected_year_2', None)
        self.selectedMo = params.get('selected_mo', None)
        self.selectedSmo = params.get('selected_smo', None)
        self.nosologies = DataReader().get_nosologies()

        if self.selectedMo != 'null' and self.selectedSmo != 'null':
            self.selectedMo = self.selectedMo.split(',')
            self.selectedMo = [int(val) for val in self.selectedMo]
            self.selectedSmo = self.selectedSmo.split(',')
            self.selectedSmo = [int(val) for val in self.selectedSmo]
        else:
            self.selectedSmo = None
            self.selectedMo = None

    def filter_data(self, data_frame, column, cond=None, gt=None, lt=None):
        u"""
        Синтаксический сахар для фильтрации DataFrame,

        :param data_frame:
        :return: slice_data_frame
        """
        slice_df = data_frame
        if cond:
            if type(cond) == list:
                slice_df = data_frame[data_frame[column].isin(cond)]
            else:
                slice_df = data_frame[data_frame[column] == cond]
        if gt and lt:
            slice_df = data_frame[(data_frame[column] >= gt) & (data_frame[column] <= lt)]
        else:
            if gt:
                slice_df = data_frame[data_frame[column] >=  gt]
            if lt:
                slice_df = data_frame[data_frame[column] <= lt]

        return slice_df

    def convert_data(self):
        u"""
        создает словарь,
        заполняя его отфильтрованными DataFrame значениями

        :return: illness_data_dict :type dict
        """
        illness_data_dict = {}
        for smo in self.selectedSmo:
            illness_data_dict[smo] = {}
            slice = self.filter_data(self.query, 'smo_id', cond=int(smo))
            for mo in self.selectedMo:
                illness_data_dict[smo][mo] = []
                slice = self.filter_data(slice, 'lpu', cond=int(mo))
                slice_amb = self.filter_data(slice, 'stat_or_amb', cond=3)
                slice_stat = self.filter_data(slice, 'stat_or_amb', cond=[1,2])
                slice_statzam = slice[slice.stat_or_amb.isna()]
                slice_skormp = self.filter_data(slice, 'stat_or_amb', cond=4)
                sum_amb = 0
                sum_stat = 0
                sum_stat_zam = 0
                sum_skor_mp = 0
                for number, _obj in enumerate(self.nosologies):
                    row = [0 for j in range(7)]
                    row[0] = _obj.number
                    row[1] = _obj.name
                    row[2] = (
                            _obj.mkbFirst + ' - ' + _obj.mkbLast) if _obj.mkbFirst != _obj.mkbLast else _obj.mkbFirst
                    count_amb = len(self.filter_data(slice_amb, 'mkb', gt=_obj.mkbFirst, lt=_obj.mkbLast))
                    count_stat = len(self.filter_data(slice_stat, 'mkb', gt=_obj.mkbFirst, lt=_obj.mkbLast))
                    count_stat_zam = len(self.filter_data(slice_statzam, 'mkb', gt=_obj.mkbFirst, lt=_obj.mkbLast))
                    count_skor_mp = len(self.filter_data(slice_skormp, 'mkb', gt=_obj.mkbFirst, lt=_obj.mkbLast))
                    row[3] = count_amb
                    row[4] = count_stat
                    row[5] = count_stat_zam
                    row[6] = count_skor_mp
                    illness_data_dict[smo][mo].append(row)
                    sum_amb += count_amb
                    sum_stat += count_stat
                    sum_stat_zam += count_stat_zam
                    sum_skor_mp += count_skor_mp
                # последняя строка
                row = [0 for j in range(7)]
                row[0] = '..'
                row[1] = 'Итого:'
                row[2] = '.....'
                row[3] = sum_amb
                row[4] = sum_stat
                row[5] = sum_stat_zam
                row[6] = sum_skor_mp
                illness_data_dict[smo][mo].append(row)
        return illness_data_dict

    def return_data_illness(self, f_dict, s_dict):
        u"""
        Функция берет 2 словаря,
        сравнивает значения в них - пересчитывает их в отдельный словарь, который и уходит в отчет
        :arg f_dict - данные по заболеваниям за отчетный месяц
        :arg s_dict - данные по заболеваниям за отчетный месяц в предыдущем календарном году

        :return: data_for_print :type dict
        """



        for smo, mo_dict in f_dict.items():
            if str(smo) in self.selectedSmo or smo in self.selectedSmo:
                for mo, rows in mo_dict.items():
                    if str(mo) in self.selectedMo or mo in self.selectedMo:
                        for j, row in enumerate(rows):
                            for i in range(3, 7, 1):
                                f_dict[smo][mo][j][i] = get_column( f_dict[smo][mo][j][i],
                                                                            s_dict[smo][mo][j][i])
        return f_dict

    def get_names_list(self):
        u"""
        Возвращает список наименований организаций

        :return: names :type list
        """
        names = {}

        for smo in self.selectedSmo:
            names[smo] = Smo_names.objects.using('dictadmin').filter(smo_id=int(smo)).values_list('short_name',
                                                                                                   flat=True)
            if len(names[smo]) > 0:
                names[smo] = names[smo][0]
            else:
                names[smo] = u'Неизвестно'
        for mo in self.selectedMo:
            names[str(mo)] = Lpu_names.objects.using('dictadmin').filter(lpu_id=int(mo)).values_list('name_short', flat=True)[0]
        return names

    def view_coordination_illness(self, request, *args):
        u"""
        Конструктор, собирающий все данные, попадающие в отчет
        :param request:
        :param args:
        :return: render
        """
        names = None
        output_data = None
        if request.method == 'GET':
            self.setup_Settings(request.GET)

            data = pd.read_csv('data/all_cases', index_col=0, parse_dates=True)
            data = data.rename(columns={'caseZid__zap_id__smo_id' : 'smo_id',
                                        'caseZid__lpu' : 'lpu',
                                        'caseZid__stat_or_amb' : 'stat_or_amb',
                                        'mkbExtra' : 'mkb',
                                        'caseZid__dateBeg' : 'begDate',
                                        'caseZid__dateEnd' : 'endDate',
                                        'caseZid__result' : 'result',
                                        'caseZid__zap_id__date_birth' : 'birthDate'})
            d_reader = DataReader()
            all_smo = d_reader.load_model_smo_names()
            all_mo = d_reader.load_model_mo_names()
            if self.selectedSmo and self.selectedMo:
                if args:
                    data = self.filter_data(data, 'birthDate', gt=calculate_date(args)[0], lt=calculate_date(args)[1])
                names = self.get_names_list()
                daterange = get_daterange(self.dateYear1, self.dateMonth1)
                data = self.filter_data(data, 'smo_id', cond = self.selectedSmo)
                self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1] )
                first_data_illness = self.convert_data()
                daterange = get_daterange(self.dateYear2, self.dateMonth2)
                self.query = self.filter_data(data, 'endDate', gt=daterange[0], lt=daterange[1])
                second_data_illness = self.convert_data()
                output_data = self.return_data_illness(first_data_illness, second_data_illness)
            return render(request, 'coordination_illness.html', {   'smo_data'   : all_smo,
                                                                'mo_data'    : all_mo,
                                                                'names_list' : names,
                                                                'data'       : output_data})

