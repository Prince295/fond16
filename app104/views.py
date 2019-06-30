import pandas as pd
import pickle
import os
import copy
import json

from django_pandas.managers import DataFrameManager
from django_pandas.io import read_frame

from django.shortcuts import render, resolve_url
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest,HttpResponseRedirect, StreamingHttpResponse
from django.conf import settings
from django.db.models import Count,Q
from django.db.models.functions import Length
from django.utils import timezone
from dateutil import relativedelta
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required

from .views_utils import copy_data, get_daterange, get_column, is_leap_year, \
    calculate_date, get_data_to_result_header, MKB_CLASS_RANGE, MKB_CLASS_RANGE_ROMAN, \
    roman_to_arabic, arabic_to_str, arabic_to_roman,  get_daterange_prev_period, get_date_to_show, \
    set_mkb_to_finder, get_smo_length
from .models import SLS, Nosologies, Mkb, Lpu_names, Patients, Z_SLS, Smo_names


global _names, _all_data, _data, _lpu_names
_all_data = False
_data = []
_names = {}  #присваивает названия лпшушкам и смошкам в отчете
_lpu_names = {}

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

        return render(request, 'coordination_illness_rebase.html', {'user' : user})
    else:
        return render(request, 'coordination_illness_rebase.html')

def logout_func(request):
    logout(request)
    return render(request, 'coordination_illness_rebase.html')



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
        load_data_old(request)
    return _data, lpus

def load_data_old(request):
    if not _data:
        daterange = ["2019-03-01", "2019-03-31"]
        nosologies = Nosologies.objects.all().order_by('id')
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
            lpu_list.append(SLS.objects.select_related('caseZid').filter(dateBeg__range=daterange).filter(lpuId__startswith=v, caseZid__stat_or_amb=3).annotate(
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

    all_smo = Smo_names.objects.using('dictadmin').all()
    all_mo = Lpu_names.objects.using('dictadmin').all()
    return render(request, 'coordination_illness_rebase.html', {'smo_data' : all_smo,
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
    Данная вьюха выглядит максимально готовой
    ( тут нужна только оптимизация разделения случаев на амбулаторные и стационарные)
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
        load_data_old(request)
    return _data, lpus

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
                    'caseZid__dateEnd', 'caseZid__result', 'caseZid__for_pom', 'goalId',
                            'caseZid__zap_id__date_birth')
        return read_frame(cases)

    def load_model_smo_names(self):
        return Smo_names.objects.using('dictadmin').all()

    def load_model_mo_names(self):
        return Lpu_names.objects.using('dictadmin').all()

    def get_nosologies(self):
        return Nosologies.objects.all().order_by('id')

    def get_MKB_classnames(self):
        all_mkb =  Mkb.objects.all().order_by('diagid').values_list('classid', 'classname')
        classnames = {}
        for mkb in all_mkb:
            classnames[arabic_to_str(roman_to_arabic(mkb[0]))] = mkb[1]
        return classnames

    def get_MKB_blocknames_filter(self, filter=None):
        u'''
        Возвращает список блоков с фильтром по классу
        :param filter:
        :return: :type dict {key : (val1, val2)}
        '''
        class_id  = '----'
        blocknames = {}
        for k, v in MKB_CLASS_RANGE_ROMAN.items():
            if v == filter:
                class_id = k
        mkbs = Mkb.objects.all().order_by('diagid').filter(classid=class_id).values_list('classid', 'blockid', 'blockname')
        counts = 1
        used_blocks = []

        for mkb in mkbs:
            if mkb[1] not in used_blocks:
                blocknames[arabic_to_str(roman_to_arabic(mkb[0])) + '.' + str(counts)] = (mkb[1], mkb[2])
                counts += 1
                used_blocks.append(mkb[1])

        return blocknames


    def get_MKB_blocknames(self):
        u"""
        Возвращает список классов и блоков
        :return:
        """
        classnames = self.get_MKB_classnames()
        blocknames = {}
        all_mkb = Mkb.objects.all().order_by('diagid').values_list('classid', 'blockid', 'blockname')
        counts = {}
        used_blocks = []
        for key in MKB_CLASS_RANGE_ROMAN.keys():
            counts[key] = 1
        for mkb in all_mkb:
            blocknames[arabic_to_str(roman_to_arabic(mkb[0]))] = classnames[arabic_to_str(roman_to_arabic(mkb[0]))]
            if mkb[1] not in used_blocks:
                blocknames[arabic_to_str(roman_to_arabic(mkb[0])) + '.' + str(counts[mkb[0]])] = (mkb[1], mkb[2])
                counts[mkb[0]] += 1
                used_blocks.append(mkb[1])
        return blocknames

    def get_all_smo_data(self):
        classnames = self.get_MKB_classnames()
        smo_objects = self.load_model_smo_names().values('smo_id', 'short_name')
        mo_objects = self.load_model_mo_names().values('lpu_id', 'name_short')


class CoordinationBase():
    u"""
    Базовый класс для построения табличного отчета по координационному совету
    """
    class_all_data = pd.read_csv('data/all_cases', index_col=0, parse_dates=True).rename(
        columns={'caseZid__zap_id__smo_id': 'smo_id',
                 'caseZid__lpu': 'lpu',
                 'caseZid__stat_or_amb': 'stat_or_amb',
                 'mkbExtra': 'mkb',
                 'caseZid__dateBeg': 'begDate',
                 'caseZid__dateEnd': 'endDate',
                 'caseZid__result': 'result',
                 'caseZid__zap_id__date_birth': 'birthDate'})

    def __init__(self):
        self.dateMonth1 = None # type: int
        self.dateYear1 = None # type: int
        self.dateMonth2 = None # type: int
        self.dateYear2 = None # type: int
        self.selectedSmo = None # type: list
        self.selectedMo = None # type: list

        self.loadedData = None
        self.loadedData_month = None
        self.loadedData_year = None
        self.nosologies = None # type: django.QuerySet
        self.query = None # type: pandas.DataFrame
        self.query_copy = None #type: pandas.DataFrame

        self._all_data = None
        self.download_null = None
        self.colorDiff = None
        self.to_percent = None


    def get_loaded_data_month(self):
        return self.loadedData_month

    def get_loaded_data_year(self):
        return self.loadedData_year

    def set_all_data(self, value):
        self._all_data = value

    @staticmethod
    def get_all_data(self):
        return self._all_data

    def filter_data(self, data_frame, column, cond=None, gt=None, lt=None, l=None):
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
        elif gt and l:
            slice_df = data_frame[(data_frame[column] >= gt) & (data_frame[column] < l)]
        else:
            if gt:
                slice_df = data_frame[data_frame[column] >=  gt]
            if lt:
                slice_df = data_frame[data_frame[column] <= lt]

        return slice_df


    def get_all_smo_data(self, current_result = None ):
        u"""
        заполняет классами нозологий
        для всех смо для всех мо
        :param current_result - уже имеющийся словарь по нозологиям, в который добавляются сравниваемые значения
        :return:
        """
        classnames = DataReader().get_MKB_classnames()
        smo_objects = DataReader().load_model_smo_names().values('smo_id', 'short_name')
        mo_objects = DataReader().load_model_mo_names().values('lpu_id', 'name_short')
        slice_amb = self.filter_data(self.query, 'stat_or_amb', cond=3)
        slice_stat = self.filter_data(self.query, 'stat_or_amb', cond=[1.0, 2.0])
        slice_statzam = self.query[self.query.stat_or_amb.isna()]
        slice_skormp = self.filter_data(self.query, 'stat_or_amb', cond=4)
        if not current_result: result_data = {}
        for smo in smo_objects:
            smo_slice = self.filter_data(self.query, 'smo_id', cond = smo['smo_id'])
            smo_slice_amb = self.filter_data(slice_amb, 'smo_id', cond = smo['smo_id'])
            smo_slice_stat = self.filter_data(slice_stat, 'smo_id', cond= smo['smo_id'])
            smo_slice_statzam = self.filter_data(slice_statzam, 'smo_id', cond=smo['smo_id'])
            smo_slice_skormp = self.filter_data(slice_skormp, 'smo_id', cond = smo['smo_id'])
            smo_sum = len(smo_slice)
            smo_sum_amb = len(smo_slice_amb)
            smo_sum_stat = len(smo_slice_stat)
            smo_sum_statzam = len(smo_slice_statzam)
            smo_sum_skormp = len (smo_slice_skormp)
            _smo = smo['smo_id']
            if not current_result: result_data[_smo] =  {}
            for mo in mo_objects:
                mo_slice = self.filter_data(smo_slice, 'lpu', cond=mo['lpu_id'])
                mo_slice_amb = self.filter_data(smo_slice_amb, 'lpu', cond=mo['lpu_id'])
                mo_slice_stat = self.filter_data(smo_slice_stat, 'lpu', cond=mo['lpu_id'])
                mo_slice_statzam = self.filter_data(smo_slice_statzam, 'lpu', cond=mo['lpu_id'])
                mo_slice_skormp = self.filter_data(smo_slice_skormp, 'lpu', cond=mo['lpu_id'])
                mo_sum = len(mo_slice)
                mo_sum_amb = len(mo_slice_amb)
                mo_sum_stat = len(mo_slice_stat)
                mo_sum_statzam = len(mo_slice_statzam)
                mo_sum_skormp = len(mo_slice_skormp)
                _mo = mo['lpu_id']
                if not current_result:
                    result_data[_smo][_mo] = {
                        '01'+classnames['01']+u'(A00-B99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='A00', l=set_mkb_to_finder('B99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='A00', l=set_mkb_to_finder('B99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='A00', l=set_mkb_to_finder('B99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='A00', l=set_mkb_to_finder('B99')))],
                        '02'+classnames['02']+u'(C00-D48)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='C00', l=set_mkb_to_finder('D48'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='C00', l=set_mkb_to_finder('D48'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='C00', l=set_mkb_to_finder('D48'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='C00', l=set_mkb_to_finder('D48')))],
                        '03'+classnames['03']+u'(D50-D99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='D50', l=set_mkb_to_finder('D99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='D50', l=set_mkb_to_finder('D99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='D50', l=set_mkb_to_finder('D99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='D50', l=set_mkb_to_finder('D99')))],
                        '04'+classnames['04']+u'(E00-E99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='E00', l=set_mkb_to_finder('E99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='E00', l=set_mkb_to_finder('E99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='E00', l=set_mkb_to_finder('E99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='E00', l=set_mkb_to_finder('E99')))],
                        '05'+classnames['05']+u'(F00-F99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='F00', l=set_mkb_to_finder('F99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='F00', l=set_mkb_to_finder('F99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='F00', l=set_mkb_to_finder('F99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='F00', l=set_mkb_to_finder('F99')))],
                        '06'+classnames['06']+u'(G00-G99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='G00', l=set_mkb_to_finder('G99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='G00', l=set_mkb_to_finder('G99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='G00', l=set_mkb_to_finder('G99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='G00', l=set_mkb_to_finder('G99')))],
                        '07'+classnames['07']+u'(H00-H59)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='H00', l=set_mkb_to_finder('H59'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='H00', l=set_mkb_to_finder('H59'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='H00', l=set_mkb_to_finder('H59'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='H00', l=set_mkb_to_finder('H59')))],
                        '08'+classnames['08']+u'(H60-H95)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='H60', l=set_mkb_to_finder('H95'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='H60', l=set_mkb_to_finder('H95'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='H60', l=set_mkb_to_finder('H95'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='H60', l=set_mkb_to_finder('H95')))],
                        '09'+classnames['09']+u'(I00-I99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='I00', l=set_mkb_to_finder('I99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='I00', l=set_mkb_to_finder('I99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='I00', l=set_mkb_to_finder('I99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='I00', l=set_mkb_to_finder('I99')))],
                        '10'+classnames['10']+u'(J00-J99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='J00', l=set_mkb_to_finder('J99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='J00', l=set_mkb_to_finder('J99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='J00', l=set_mkb_to_finder('J99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='J00', l=set_mkb_to_finder('J99')))],
                        '11'+classnames['11']+u'(K00-K93)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='K00', l=set_mkb_to_finder('K93'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='K00', l=set_mkb_to_finder('K93'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='K00', l=set_mkb_to_finder('K93'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='K00', l=set_mkb_to_finder('K93')))],
                        '12'+classnames['12']+u'(L00-L99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='L00', l=set_mkb_to_finder('L99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='L00', l=set_mkb_to_finder('L99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='L00', l=set_mkb_to_finder('L99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='L00', l=set_mkb_to_finder('L99')))],
                        '13'+classnames['13']+u'(M00-M99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='M00', l=set_mkb_to_finder('M99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='M00', l=set_mkb_to_finder('M99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='M00', l=set_mkb_to_finder('M99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='M00', l=set_mkb_to_finder('M99')))],
                        '14'+classnames['14']+u'(N00-N99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='N00', l=set_mkb_to_finder('N99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='N00', l=set_mkb_to_finder('N99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='N00', l=set_mkb_to_finder('N99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='N00', l=set_mkb_to_finder('N99')))],
                        '15'+classnames['15']+u'(O00-O99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='O00', l=set_mkb_to_finder('O99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='O00', l=set_mkb_to_finder('O99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='O00', l=set_mkb_to_finder('O99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='O00', l=set_mkb_to_finder('O99')))],
                        '16'+classnames['16']+u'(P00-P96)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='P00', l=set_mkb_to_finder('P96'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='P00', l=set_mkb_to_finder('P96'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='P00', l=set_mkb_to_finder('P96'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='P00', l=set_mkb_to_finder('P96')))],
                        '17'+classnames['17']+u'(Q00-Q99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99')))],
                        '18'+classnames['18']+u'(R00-R99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='R00', l=set_mkb_to_finder('R99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='R00', l=set_mkb_to_finder('R99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='R00', l=set_mkb_to_finder('R99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='R00', l=set_mkb_to_finder('R99')))],
                        '19'+classnames['19']+u'(S00-T98)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='S00', l=set_mkb_to_finder('T98'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='S00', l=set_mkb_to_finder('T98'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='S00', l=set_mkb_to_finder('T98'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='S00', l=set_mkb_to_finder('T98')))],
                        '20'+classnames['20']+u'(V01-Y98)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='V01', l=set_mkb_to_finder('Y98'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='V01', l=set_mkb_to_finder('Y98'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='V01', l=set_mkb_to_finder('Y98'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='V01', l=set_mkb_to_finder('Y98')))],
                        '21'+classnames['21']+u'(Z00-Z99)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99'))),
                                                             len(self.filter_data(mo_slice_stat, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99'))),
                                                             len(self.filter_data(mo_slice_statzam, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99'))),
                                                             len(self.filter_data(mo_slice_skormp, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99')))],
                        # '22'+classnames['22']+u'(U00-U85)': [len(self.filter_data(mo_slice_amb, 'mkb', gt='U00', l=set_mkb_to_finder('U85'))),
                        #                                      len(self.filter_data(mo_slice_stat, 'mkb', gt='U00', l=set_mkb_to_finder('U85'))),
                        #                                      len(self.filter_data(mo_slice_statzam, 'mkb', gt='U00', l=set_mkb_to_finder('U85'))),
                        #                                      len(self.filter_data(mo_slice_skormp, 'mkb', gt='U00', l=set_mkb_to_finder('U85')))
                        }
                    result_data[_smo][_mo]['Итого'] = [mo_sum_amb, mo_sum_stat, mo_sum_statzam, mo_sum_skormp]
                else:
                    current_result[_smo][_mo]['01'+classnames['01']+u'(A00-B99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='A00', l=set_mkb_to_finder('B99'))))
                    current_result[_smo][_mo]['01' + classnames['01'] + u'(A00-B99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='A00', l=set_mkb_to_finder('B99'))))
                    current_result[_smo][_mo]['01' + classnames['01'] + u'(A00-B99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='A00', l=set_mkb_to_finder('B99'))))
                    current_result[_smo][_mo]['01' + classnames['01'] + u'(A00-B99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='A00', l=set_mkb_to_finder('B99'))))
                    current_result[_smo][_mo]['02' + classnames['02'] + u'(C00-D48)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='C00', l=set_mkb_to_finder('D48'))))
                    current_result[_smo][_mo]['02' + classnames['02'] + u'(C00-D48)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='C00', l=set_mkb_to_finder('D48'))))
                    current_result[_smo][_mo]['02' + classnames['02'] + u'(C00-D48)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='C00', l=set_mkb_to_finder('D48'))))
                    current_result[_smo][_mo]['02' + classnames['02'] + u'(C00-D48)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='C00', l=set_mkb_to_finder('D48'))))
                    current_result[_smo][_mo]['03' + classnames['03'] + u'(D50-D99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='D50', l=set_mkb_to_finder('D99'))))
                    current_result[_smo][_mo]['03' + classnames['03'] + u'(D50-D99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='D50', l=set_mkb_to_finder('D99'))))
                    current_result[_smo][_mo]['03' + classnames['03'] + u'(D50-D99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='D50', l=set_mkb_to_finder('D99'))))
                    current_result[_smo][_mo]['03' + classnames['03'] + u'(D50-D99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='D50', l=set_mkb_to_finder('D99'))))
                    current_result[_smo][_mo]['04' + classnames['04'] + u'(E00-E99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='E00', l=set_mkb_to_finder('E99'))))
                    current_result[_smo][_mo]['04' + classnames['04'] + u'(E00-E99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='E00', l=set_mkb_to_finder('E99'))))
                    current_result[_smo][_mo]['04' + classnames['04'] + u'(E00-E99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='E00', l=set_mkb_to_finder('E99'))))
                    current_result[_smo][_mo]['04' + classnames['04'] + u'(E00-E99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='E00', l=set_mkb_to_finder('E99'))))
                    current_result[_smo][_mo]['05' + classnames['05'] + u'(F00-F99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='F00', l=set_mkb_to_finder('F99'))))
                    current_result[_smo][_mo]['05' + classnames['05'] + u'(F00-F99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='F00', l=set_mkb_to_finder('F99'))))
                    current_result[_smo][_mo]['05' + classnames['05'] + u'(F00-F99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='F00', l=set_mkb_to_finder('F99'))))
                    current_result[_smo][_mo]['05' + classnames['05'] + u'(F00-F99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='F00', l=set_mkb_to_finder('F99'))))
                    current_result[_smo][_mo]['06' + classnames['06'] + u'(G00-G99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='G00', l=set_mkb_to_finder('G99'))))
                    current_result[_smo][_mo]['06' + classnames['06'] + u'(G00-G99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='G00', l=set_mkb_to_finder('G99'))))
                    current_result[_smo][_mo]['06' + classnames['06'] + u'(G00-G99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='G00', l=set_mkb_to_finder('G99'))))
                    current_result[_smo][_mo]['06' + classnames['06'] + u'(G00-G99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='G00', l=set_mkb_to_finder('G99'))))
                    current_result[_smo][_mo]['07' + classnames['07'] + u'(H00-H59)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='H00', l=set_mkb_to_finder('H59'))))
                    current_result[_smo][_mo]['07' + classnames['07'] + u'(H00-H59)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='H00', l=set_mkb_to_finder('H59'))))
                    current_result[_smo][_mo]['07' + classnames['07'] + u'(H00-H59)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='H00', l=set_mkb_to_finder('H59'))))
                    current_result[_smo][_mo]['07' + classnames['07'] + u'(H00-H59)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='H00', l=set_mkb_to_finder('H59'))))
                    current_result[_smo][_mo]['08' + classnames['08'] + u'(H60-H95)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='H60', l=set_mkb_to_finder('H95'))))
                    current_result[_smo][_mo]['08' + classnames['08'] + u'(H60-H95)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='H60', l=set_mkb_to_finder('H95'))))
                    current_result[_smo][_mo]['08' + classnames['08'] + u'(H60-H95)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='H60', l=set_mkb_to_finder('H95'))))
                    current_result[_smo][_mo]['08' + classnames['08'] + u'(H60-H95)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='H60', l=set_mkb_to_finder('H95'))))
                    current_result[_smo][_mo]['09' + classnames['09'] + u'(I00-I99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='I00', l=set_mkb_to_finder('I99'))))
                    current_result[_smo][_mo]['09' + classnames['09'] + u'(I00-I99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='I00', l=set_mkb_to_finder('I99'))))
                    current_result[_smo][_mo]['09' + classnames['09'] + u'(I00-I99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='I00', l=set_mkb_to_finder('I99'))))
                    current_result[_smo][_mo]['09' + classnames['09'] + u'(I00-I99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='I00', l=set_mkb_to_finder('I99'))))
                    current_result[_smo][_mo]['10' + classnames['10'] + u'(J00-J99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='J00', l=set_mkb_to_finder('J99'))))
                    current_result[_smo][_mo]['10' + classnames['10'] + u'(J00-J99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='J00', l=set_mkb_to_finder('J99'))))
                    current_result[_smo][_mo]['10' + classnames['10'] + u'(J00-J99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='J00', l=set_mkb_to_finder('J99'))))
                    current_result[_smo][_mo]['10' + classnames['10'] + u'(J00-J99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='J00', l=set_mkb_to_finder('J99'))))
                    current_result[_smo][_mo]['11' + classnames['11'] + u'(K00-K93)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='K00', l=set_mkb_to_finder('K93'))))
                    current_result[_smo][_mo]['11' + classnames['11'] + u'(K00-K93)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='K00', l=set_mkb_to_finder('K93'))))
                    current_result[_smo][_mo]['11' + classnames['11'] + u'(K00-K93)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='K00', l=set_mkb_to_finder('K93'))))
                    current_result[_smo][_mo]['11' + classnames['11'] + u'(K00-K93)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='K00', l=set_mkb_to_finder('K93'))))
                    current_result[_smo][_mo]['12' + classnames['12'] + u'(L00-L99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='L00', l=set_mkb_to_finder('L99'))))
                    current_result[_smo][_mo]['12' + classnames['12'] + u'(L00-L99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='L00', l=set_mkb_to_finder('L99'))))
                    current_result[_smo][_mo]['12' + classnames['12'] + u'(L00-L99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='L00', l=set_mkb_to_finder('L99'))))
                    current_result[_smo][_mo]['12' + classnames['12'] + u'(L00-L99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='L00', l=set_mkb_to_finder('L99'))))
                    current_result[_smo][_mo]['13' + classnames['13'] + u'(M00-M99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='M00', l=set_mkb_to_finder('M99'))))
                    current_result[_smo][_mo]['13' + classnames['13'] + u'(M00-M99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='M00', l=set_mkb_to_finder('M99'))))
                    current_result[_smo][_mo]['13' + classnames['13'] + u'(M00-M99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='M00', l=set_mkb_to_finder('M99'))))
                    current_result[_smo][_mo]['13' + classnames['13'] + u'(M00-M99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='M00', l=set_mkb_to_finder('M99'))))
                    current_result[_smo][_mo]['14' + classnames['14'] + u'(N00-N99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='N00', l=set_mkb_to_finder('N99'))))
                    current_result[_smo][_mo]['14' + classnames['14'] + u'(N00-N99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='N00', l=set_mkb_to_finder('N99'))))
                    current_result[_smo][_mo]['14' + classnames['14'] + u'(N00-N99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='N00', l=set_mkb_to_finder('N99'))))
                    current_result[_smo][_mo]['14' + classnames['14'] + u'(N00-N99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='N00', l=set_mkb_to_finder('N99'))))
                    current_result[_smo][_mo]['15' + classnames['15'] + u'(O00-O99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='O00', l=set_mkb_to_finder('O99'))))
                    current_result[_smo][_mo]['15' + classnames['15'] + u'(O00-O99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='O00', l=set_mkb_to_finder('O99'))))
                    current_result[_smo][_mo]['15' + classnames['15'] + u'(O00-O99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='O00', l=set_mkb_to_finder('O99'))))
                    current_result[_smo][_mo]['15' + classnames['15'] + u'(O00-O99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='O00', l=set_mkb_to_finder('O99'))))
                    current_result[_smo][_mo]['16' + classnames['16'] + u'(P00-P96)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='P00', l=set_mkb_to_finder('P96'))))
                    current_result[_smo][_mo]['16' + classnames['16'] + u'(P00-P96)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='P00', l=set_mkb_to_finder('P96'))))
                    current_result[_smo][_mo]['16' + classnames['16'] + u'(P00-P96)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='P00', l=set_mkb_to_finder('P96'))))
                    current_result[_smo][_mo]['16' + classnames['16'] + u'(P00-P96)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='P00', l=set_mkb_to_finder('P96'))))
                    current_result[_smo][_mo]['17' + classnames['17'] + u'(Q00-Q99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99'))))
                    current_result[_smo][_mo]['17' + classnames['17'] + u'(Q00-Q99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99'))))
                    current_result[_smo][_mo]['17' + classnames['17'] + u'(Q00-Q99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99'))))
                    current_result[_smo][_mo]['17' + classnames['17'] + u'(Q00-Q99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='Q00', l=set_mkb_to_finder('Q99'))))
                    current_result[_smo][_mo]['18' + classnames['18'] + u'(R00-R99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='R00', l=set_mkb_to_finder('R99'))))
                    current_result[_smo][_mo]['18' + classnames['18'] + u'(R00-R99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='R00', l=set_mkb_to_finder('R99'))))
                    current_result[_smo][_mo]['18' + classnames['18'] + u'(R00-R99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='R00', l=set_mkb_to_finder('R99'))))
                    current_result[_smo][_mo]['18' + classnames['18'] + u'(R00-R99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='R00', l=set_mkb_to_finder('R99'))))
                    current_result[_smo][_mo]['19' + classnames['19'] + u'(S00-T98)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='S00', l=set_mkb_to_finder('T98'))))
                    current_result[_smo][_mo]['19' + classnames['19'] + u'(S00-T98)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='S00', l=set_mkb_to_finder('T98'))))
                    current_result[_smo][_mo]['19' + classnames['19'] + u'(S00-T98)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='S00', l=set_mkb_to_finder('T98'))))
                    current_result[_smo][_mo]['19' + classnames['19'] + u'(S00-T98)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='S00', l=set_mkb_to_finder('T98'))))
                    current_result[_smo][_mo]['20' + classnames['20'] + u'(V01-Y98)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='V01', l=set_mkb_to_finder('Y98'))))
                    current_result[_smo][_mo]['20' + classnames['20'] + u'(V01-Y98)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='V01', l=set_mkb_to_finder('Y98'))))
                    current_result[_smo][_mo]['20' + classnames['20'] + u'(V01-Y98)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='V01', l=set_mkb_to_finder('Y98'))))
                    current_result[_smo][_mo]['20' + classnames['20'] + u'(V01-Y98)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='V01', l=set_mkb_to_finder('Y98'))))
                    current_result[_smo][_mo]['21' + classnames['21'] + u'(Z00-Z99)'].append(
                        len(self.filter_data(mo_slice_amb, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99'))))
                    current_result[_smo][_mo]['21' + classnames['21'] + u'(Z00-Z99)'].append(
                        len(self.filter_data(mo_slice_stat, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99'))))
                    current_result[_smo][_mo]['21' + classnames['21'] + u'(Z00-Z99)'].append(
                        len(self.filter_data(mo_slice_statzam, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99'))))
                    current_result[_smo][_mo]['21' + classnames['21'] + u'(Z00-Z99)'].append(
                        len(self.filter_data(mo_slice_skormp, 'mkb', gt='Z00', l=set_mkb_to_finder('Z99'))))
                    # current_result[_smo][_mo]['22' + classnames['22'] + u'(U00-U85)'].append(
                    #     len(self.filter_data(mo_slice_amb, 'mkb', gt='U00', l=set_mkb_to_finder('U85'))))
                    # current_result[_smo][_mo]['22' + classnames['22'] + u'(U00-U85)'].append(
                    #     len(self.filter_data(mo_slice_stat, 'mkb', gt='U00', l=set_mkb_to_finder('U85'))))
                    # current_result[_smo][_mo]['22' + classnames['22'] + u'(U00-U85)'].append(
                    #     len(self.filter_data(mo_slice_statzam, 'mkb', gt='U00', l=set_mkb_to_finder('U85'))))
                    # current_result[_smo][_mo]['22' + classnames['22'] + u'(U00-U85)'].append(
                    #     len(self.filter_data(mo_slice_skormp, 'mkb', gt='U00', l=set_mkb_to_finder('U85'))))
                    current_result[_smo][_mo]['Итого'].append(mo_sum_amb)
                    current_result[_smo][_mo]['Итого'].append(mo_sum_stat)
                    current_result[_smo][_mo]['Итого'].append(mo_sum_statzam)
                    current_result[_smo][_mo]['Итого'].append(mo_sum_skormp)
            if not current_result:
                result_data[_smo]['all'] = {'Итого' : [smo_sum_amb, smo_sum_stat, smo_sum_statzam, smo_sum_skormp]}
            else:
                current_result[_smo]['all']['Итого'].append(smo_sum_amb)
                current_result[_smo]['all']['Итого'].append(smo_sum_stat)
                current_result[_smo]['all']['Итого'].append(smo_sum_statzam)
                current_result[_smo]['all']['Итого'].append(smo_sum_skormp)
        if not current_result:
            return result_data
        else:
            return current_result


    def get_blockname_data(self, smo, mo, year, month,  classname, dataframe, is_death=True):
        u"""
        Вернет данные по блоку,
        в зависимости от класса, мо, смо
        :param classname:
        :return: :type: dict
        """

        death_list = [105, 106, 205, 206, 313, 405, 406, 411]
        mo = int(mo)
        smo = int(smo)
        classname = classname[0:2]
        self._all_data = dataframe
        mkb_range = MKB_CLASS_RANGE.get(classname)
        if mkb_range:
            blocks = DataReader().get_MKB_blocknames_filter(mkb_range)

        nos_rows = {}
        if is_death:
            self._all_data = self.filter_data(self._all_data, 'result', cond=death_list)
        daterange = get_daterange(year, month)
        first_period = self.filter_data(self._all_data,'begDate', gt=daterange[0], lt=daterange[1])
        daterange_m = get_daterange_prev_period(daterange, prev_month=True)
        daterange_y = get_daterange_prev_period(daterange, prev_year=True)
        second_period = self.filter_data(self._all_data, 'begDate', gt=daterange_m[0], lt=daterange_m[1])
        third_period = self.filter_data(self._all_data, 'begDate', gt=daterange_y[0], lt= daterange_y[1])

        smo_filter = self.filter_data(first_period, 'smo_id', cond=smo)
        mo_filter = self.filter_data(smo_filter, 'lpu', cond=mo)
        slice_amb = self.filter_data(mo_filter, 'stat_or_amb', cond=3)
        slice_stat = self.filter_data(mo_filter, 'stat_or_amb', cond=[1, 2])
        slice_statzam = mo_filter[mo_filter.stat_or_amb.isna()]
        slice_skormp = self.filter_data(mo_filter, 'stat_or_amb', cond=4)

        smo_filter_m = self.filter_data(second_period, 'smo_id', cond=smo)
        mo_filter_m = self.filter_data(smo_filter_m, 'lpu', cond=mo)
        slice_amb_m = self.filter_data(mo_filter_m, 'stat_or_amb', cond=3)
        slice_stat_m = self.filter_data(mo_filter_m, 'stat_or_amb', cond=[1, 2])
        slice_statzam_m = mo_filter_m[mo_filter_m.stat_or_amb.isna()]
        slice_skormp_m = self.filter_data(mo_filter_m, 'stat_or_amb', cond=4)

        smo_filter_y = self.filter_data(third_period, 'smo_id', cond=smo)
        mo_filter_y = self.filter_data(smo_filter_y, 'lpu', cond=mo)
        slice_amb_y = self.filter_data(mo_filter_y, 'stat_or_amb', cond=3)
        slice_stat_y = self.filter_data(mo_filter_y, 'stat_or_amb', cond=[1, 2])
        slice_statzam_y = mo_filter_y[mo_filter_y.stat_or_amb.isna()]
        slice_skormp_y = self.filter_data(mo_filter_y, 'stat_or_amb', cond=4)
        for blockname, blockvals in blocks.items():
            key = blockname + blockvals[1] + blockvals[0]
            if blockvals[0].endswith('))'):
                mkb_first = blockvals[0][1:-2]
                mkb_second = mkb_first
            else:
                mkb_first = blockvals[0].split('-')[0][1:]
                mkb_second = blockvals[0].split('-')[1][:-1]

            row = [0 for i in range(12)]
            row[0] = len(self.filter_data(slice_amb, 'mkb', gt=mkb_first, lt=mkb_second))
            row[1] = len(self.filter_data(slice_stat, 'mkb', gt=mkb_first, lt=mkb_second))
            row[2] = len(self.filter_data(slice_statzam, 'mkb', gt=mkb_first, lt=mkb_second))
            row[3] = len(self.filter_data(slice_skormp, 'mkb', gt=mkb_first, lt=mkb_second))
            row[4] = len(self.filter_data(slice_amb_m, 'mkb', gt=mkb_first, lt=mkb_second))
            row[5] = len(self.filter_data(slice_stat_m, 'mkb', gt=mkb_first, lt=mkb_second))
            row[6] = len(self.filter_data(slice_statzam_m, 'mkb', gt=mkb_first, lt=mkb_second))
            row[7] = len(self.filter_data(slice_skormp_m, 'mkb', gt=mkb_first, lt=mkb_second))
            row[8] = len(self.filter_data(slice_amb_y, 'mkb', gt=mkb_first, lt=mkb_second))
            row[9] = len(self.filter_data(slice_stat_y, 'mkb', gt=mkb_first, lt=mkb_second))
            row[10] = len(self.filter_data(slice_statzam_y, 'mkb', gt=mkb_first, lt=mkb_second))
            row[11] = len(self.filter_data(slice_skormp_y, 'mkb', gt=mkb_first, lt=mkb_second))
            nos_rows[key] = row

        return nos_rows

    def save_monthly_report_data(self, report, month, year, is_death=False):
        u"""
        Сериализация и сохранение отчета в отправляемом на сервер виде
        помогает быстро подгружать основные данные в 107 форму
        :param report: данные :type dict
        :param month: месяц выгрузки
        :param year: год выгрузки
        :return: None
        """
        concat_filename = 'data/' + month + '_' + year
        if is_death:
            concat_filename += '_d'
        with open(concat_filename, 'wb') as f:
            pickle.dump(report, f)

    def load_monthly_report_data(self, month, year, is_death=False):
        u"""
        Попытка найти и загрузить данные за месяц выгрузки
        :param month:
        :param year:
        :return: report
        """
        concat_filename = 'data/' + month + '_' + year
        if is_death:
            concat_filename += '_d'
        if os.path.exists(concat_filename):
            with open(concat_filename, 'rb') as f:
                self.loadedData = pickle.load(f)
                self.loadedData_month = month
                self.loadedData_year = year
            return True
        else:
            return False

    def convert_data(self):
        u"""
        создает словарь,
        заполняя его отфильтрованными DataFrame значениями

        :return: illness_data_dict :type dict
        """
        illness_data_dict = {}
        mkb_classlist = DataReader().get_MKB_blocknames()
        for smo in self.selectedSmo:
            illness_data_dict[smo] = {}
            slice = self.filter_data(self.query, 'smo_id', cond=int(smo))
            for mo in self.selectedMo:
                illness_data_dict[smo][mo] = []
                slice_mo = self.filter_data(slice, 'lpu', cond=int(mo))
                slice_amb = self.filter_data(slice_mo, 'stat_or_amb', cond=3)
                slice_stat = self.filter_data(slice_mo, 'stat_or_amb', cond=[1,2])
                slice_statzam = slice_mo[slice_mo.stat_or_amb.isna()]
                slice_skormp = self.filter_data(slice_mo, 'stat_or_amb', cond=4)
                sum_amb = 0
                sum_stat = 0
                sum_stat_zam = 0
                sum_skor_mp = 0
                for key,_obj in mkb_classlist.items():
                    row = [0 for j in range(7)]
                    row[0] = key
                    row[1] = _obj if type(_obj) != tuple else _obj[1]
                    if len(key) <= 2:
                        mkbFirst = MKB_CLASS_RANGE.get(key, 'A00-A01').split('-')[0]
                        mkbLast = MKB_CLASS_RANGE.get(key, 'A00-A01').split('-')[1]
                    else:
                        if '-' in _obj[0]:
                            mkbFirst = _obj[0].split('-')[0][1:]
                            mkbLast = _obj[0].split('-')[1][:-1]
                        else:
                            mkbFirst = mkbLast = _obj[0][1:-2]
                    row[2] = (
                            mkbFirst + ' - ' + mkbLast) if mkbFirst != mkbLast else mkbFirst
                    count_amb = len(self.filter_data(slice_amb, 'mkb', gt=mkbFirst, lt=mkbLast))
                    count_stat = len(self.filter_data(slice_stat, 'mkb', gt=mkbFirst, lt=mkbLast))
                    count_stat_zam = len(self.filter_data(slice_statzam, 'mkb', gt=mkbFirst, lt=mkbLast))
                    count_skor_mp = len(self.filter_data(slice_skormp, 'mkb', gt=mkbFirst, lt=mkbLast))
                    row[3] = count_amb
                    row[4] = count_stat
                    row[5] = count_stat_zam
                    row[6] = count_skor_mp
                    illness_data_dict[smo][mo].append(row)
                    if len(row[0]) <= 2:
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

    def setup_Settings(self, params):
        to_bool = {'true' : True,
                   'false' : False}

        self.dateMonth1 = params.get('selected_month_1', None)
        self.dateYear1 = params.get('selected_year_1', None)
        self.dateMonth2 = params.get('selected_month_2', None)
        self.dateYear2 = params.get('selected_year_2', None)
        self.selectedMo = params.get('selected_mo', None)
        self.selectedSmo = params.get('selected_smo', None)
        self.download_null = params.get('checkboxDownload', None)
        self.to_percent = params.get('checkbox_percent', None)
        self.colorDiff = params.get('colorDiff', None)
        if self.colorDiff: self.colorDiff = to_bool.get(self.colorDiff, False)
        if self.to_percent: self.to_percent = to_bool.get(self.to_percent, False)
        if self.download_null: self.download_null = to_bool.get(self.download_null, False)
        self.nosologies = DataReader().get_nosologies()
        not_vals = ['null', '', None]
        if self.selectedMo not in not_vals and self.selectedSmo not in not_vals:
            self.selectedMo = self.selectedMo.split(',')
            self.selectedMo = [int(val) for val in self.selectedMo]
            self.selectedSmo = self.selectedSmo.split(',')
            self.selectedSmo = [int(val) for val in self.selectedSmo]
        else:
            self.selectedSmo = None
            self.selectedMo = None

    def get_check_states(self):
        result = ['', '', '']
        if self.colorDiff:
            result[0] = 'checked'
        if self.download_null:
            result[1] = 'checked'
        if self.to_percent:
            result[2] = 'checked'
        return result


    def return_data(self, f_dict, s_dict):
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
        if self.selectedSmo:
            for smo in self.selectedSmo:
                names[smo] = Smo_names.objects.using('dictadmin').filter(smo_id=int(smo)).values_list('short_name',
                                                                                                       flat=True)
                if len(names[smo]) > 0:
                    names[smo] = names[smo][0]
                else:
                    names[smo] = u'Неизвестно'
        else:
            names_dict = Smo_names.objects.using('dictadmin').values('smo_id', 'short_name')
            for it in names_dict:
                names[it['smo_id']] = it['short_name']
        if self.selectedMo:
            for mo in self.selectedMo:
                names[str(mo)] = Lpu_names.objects.using('dictadmin').filter(lpu_id=int(mo)).values_list('name_short', flat=True)[0]
        else:
            names_dict = Lpu_names.objects.using('dictadmin').values('lpu_id', 'name_short')
            for it in names_dict:
                names[it['lpu_id']] = it['name_short']
        return names

    def prepare_to_show_overall(self, data, cut_zeroes=False):
        u"""
        Вытягивает из словаря значения верхних уровней
        и итоговые суммы
        :param data:
        :return: result
        """
        keys = []
        mo_keys = []
        result = copy.deepcopy(data)
        for smo, mo_dict in data.items():
            if not any(data[smo]['all']['Итого']):
                keys.append(smo)
            for mo, values_dict in mo_dict.items():
                if not any(data[smo][mo]['Итого']):
                    mo_keys.append([smo,mo])
                for key, vals in values_dict.items():
                    if key not in ['all', 'Итого']:
                        del result[smo][mo][key]
        if cut_zeroes:
            for k in keys:
                del result[k]
            for v in mo_keys:
                if v[0] not in keys:
                    del result[v[0]][v[1]]

        return result

class Coordination_illness_views(CoordinationBase):
    def __init__(self):
        self.loadedData_year = CoordinationBase().get_loaded_data_year()
        self.loadedData_month = CoordinationBase().get_loaded_data_year()
        super(CoordinationBase, self).__init__()

    def view_empty_coordination_illness(self, request):
        u"""
        Пустая таблица отчета по заболеваемости
        :param request:
        :return:
        """

        d_reader = DataReader()
        all_smo = d_reader.load_model_smo_names()
        all_mo = d_reader.load_model_mo_names()
        return render(request, 'coordination_illness_rebase.html', {'smo_data': all_smo,
                                                             'mo_data': all_mo})

    def view_all_smo_class_names(self, request, *args):
        u"""
        Конструктор, собирающий данные по всем смо и по всем мо для каждой смо за отчетный период
        :param request:
        :param args:
        :return:
        """
        names = None
        period_1 = None
        period_2 = None
        if request.method == 'GET':
            self.setup_Settings(request.GET)
            smo_column_length = None
            check_states = self.get_check_states()
            if self.dateYear1 and self.dateMonth1:
                names = self.get_names_list()
                if self.loadedData_year == self.dateYear1 and self.loadedData_month == self.dateMonth1:
                    daterange = get_daterange(self.dateYear1, self.dateMonth1)
                    daterange = get_daterange_prev_period(daterange, prev_month=True)
                    period_1 = self.loadedData
                    period_1 = self.prepare_to_show_overall(period_1, cut_zeroes=self.download_null)
                    smo_column_length = get_smo_length(period_1)
                elif self.load_monthly_report_data(self.dateMonth1, self.dateYear1):
                    period_1 = self.loadedData
                    period_1 = self.prepare_to_show_overall(period_1, cut_zeroes=self.download_null)
                    smo_column_length = get_smo_length(period_1)
                else:
                    data = pd.read_csv('data/all_cases', index_col=0, parse_dates=True)
                    data = data.rename(columns={'caseZid__zap_id__smo_id': 'smo_id',
                                                'caseZid__lpu': 'lpu',
                                                'caseZid__stat_or_amb': 'stat_or_amb',
                                                'mkbExtra': 'mkb',
                                                'caseZid__dateBeg': 'begDate',
                                                'caseZid__dateEnd': 'endDate',
                                                'caseZid__result': 'result',
                                                'caseZid__zap_id__date_birth': 'birthDate'})
                    self.set_all_data(data)
                    daterange = get_daterange(self.dateYear1, self.dateMonth1)
                    self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1])
                    period_1 = self.get_all_smo_data()
                    daterange = get_daterange(self.dateYear1, self.dateMonth1)
                    daterange = get_daterange_prev_period(daterange, prev_month=True)
                    self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1])
                    period_1 = self.get_all_smo_data(current_result=period_1)
                    daterange = get_daterange(self.dateYear1, self.dateMonth1)
                    daterange = get_daterange_prev_period(daterange, prev_year=True)
                    self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1])
                    period_1 = self.get_all_smo_data(current_result=period_1)
                    self.save_monthly_report_data(period_1, self.dateMonth1, self.dateYear1)
                    self.loadedData = dict(period_1)
                    period_1 = self.prepare_to_show_overall(period_1, cut_zeroes=self.download_null)
                    smo_column_length = get_smo_length(period_1)


            return render(request, 'coordination_illness_rebase.html', {'check_states' : check_states,
                                                                            'first_period' :period_1,
                                                                             'names' : names,
                                                                            'smo_column_length' : smo_column_length,
                                                                            'date_to_show' : get_date_to_show(self.dateYear1, self.dateMonth1)})
            # return render(request, 'coordination_illness_rebase.html', {'first_period' : period_1 })


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
            self.set_all_data(data)
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
                self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1])
                second_data_illness = self.convert_data()
                output_data = self.return_data(first_data_illness, second_data_illness)
            return render(request, 'coordination_illness.html', {'smo_data'   : all_smo,
                                                                 'mo_data'    : all_mo,
                                                                 'names_list' : names,
                                                                 'data'       : output_data,
                                                                'month_year_1': get_data_to_result_header(self.dateMonth1, self.dateYear1),
                                                                'month_year_2': get_data_to_result_header(self.dateMonth2, self.dateYear2)})

    def view_coordination_illness_load_classes(self, request, *args):
        u"""
        Вьюха, возвращающая позиции словаря по смо, мо
        :param request:
        :param args:
        :return:
        """
        if request.method == 'GET':
            mo=request.GET.get('mo', None)
            smo=request.GET.get('smo', None)
            month = request.GET.get('month', None)
            year = request.GET.get('year', None)
            if self.loadedData_year != year and self.loadedData_month != month:
                if self.load_monthly_report_data(month, year):
                    dataset = self.loadedData
                else:
                    dataset = None
            else:
                dataset = self.loadedData
            response_dict = dataset[int(smo)][int(mo)]

            return JsonResponse(response_dict)

    def view_coordination_illness_load_blocks(self, request, *args):
        u"""
        Вьюха, возвращающая позиции словаря по смо, мо, нозологической форме
        :param request:
        :param args:
        :return:
        """
        if request.method == 'GET':
            mo=request.GET.get('mo', None)
            smo=request.GET.get('smo', None)
            month = request.GET.get('month', None)
            year = request.GET.get('year', None)
            classname = request.GET.get('classname', None)
            nos_data = self.get_blockname_data(smo, mo, year, month, classname,  dataframe=self.class_all_data)
            response_dict = nos_data

            return JsonResponse(response_dict)


class Coordination_death_views(CoordinationBase):

    def __init__(self):
        self.loadedData_year = CoordinationBase().get_loaded_data_year()
        self.loadedData_month = CoordinationBase().get_loaded_data_year()
        super(CoordinationBase, self).__init__()
        self.death_list = [105, 106, 205, 206, 313, 405, 406, 411]

    def view_empty_coordination_death(self, request):
        u"""
        Пустая таблица отчета по смертности
        :param request:
        :return:
        """

        d_reader = DataReader()
        all_smo = d_reader.load_model_smo_names()
        all_mo = d_reader.load_model_mo_names()
        return render(request, 'coordination_death_rebase.html', {'smo_data': all_smo,
                                                             'mo_data': all_mo})

    def view_all_smo_class_names(self, request, *args):
        u"""
        Конструктор, собирающий данные по всем смо и по всем мо для каждой смо за отчетный период
        :param request:
        :param args:
        :return:
        """
        names = None
        period_1 = None
        period_2 = None
        if request.method == 'GET':
            self.setup_Settings(request.GET)
            smo_column_length = None
            check_states = self.get_check_states()
            if self.dateYear1 and self.dateMonth1:
                names = self.get_names_list()
                if self.loadedData_year == self.dateYear1 and self.loadedData_month == self.dateMonth1:

                    period_1 = self.loadedData
                    period_1 = self.prepare_to_show_overall(period_1, cut_zeroes=self.download_null)
                    smo_column_length = get_smo_length(period_1)
                elif self.load_monthly_report_data(self.dateMonth1, self.dateYear1, is_death=True):
                    period_1 = self.loadedData
                    period_1 = self.prepare_to_show_overall(period_1, cut_zeroes=self.download_null)
                    smo_column_length = get_smo_length(period_1)
                else:
                    data = pd.read_csv('data/all_cases', index_col=0, parse_dates=True)
                    data = data.rename(columns={'caseZid__zap_id__smo_id': 'smo_id',
                                                'caseZid__lpu': 'lpu',
                                                'caseZid__stat_or_amb': 'stat_or_amb',
                                                'mkbExtra': 'mkb',
                                                'caseZid__dateBeg': 'begDate',
                                                'caseZid__dateEnd': 'endDate',
                                                'caseZid__result': 'result',
                                                'caseZid__zap_id__date_birth': 'birthDate'})
                    self.set_all_data(data)
                    daterange = get_daterange(self.dateYear1, self.dateMonth1)
                    data = self.filter_data(data, 'result', cond=self.death_list)
                    self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1])
                    period_1 = self.get_all_smo_data()
                    daterange = get_daterange(self.dateYear1, self.dateMonth1)
                    daterange = get_daterange_prev_period(daterange, prev_month=True)
                    self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1])
                    period_1 = self.get_all_smo_data(current_result=period_1)
                    daterange = get_daterange(self.dateYear1, self.dateMonth1)
                    daterange = get_daterange_prev_period(daterange, prev_year=True)
                    self.query = self.filter_data(data, 'begDate', gt=daterange[0], lt=daterange[1])
                    period_1 = self.get_all_smo_data(current_result=period_1)
                    self.save_monthly_report_data(period_1, self.dateMonth1, self.dateYear1, is_death=True)
                    self.loadedData = dict(period_1)
                    period_1 = self.prepare_to_show_overall(period_1, cut_zeroes=self.download_null)
                    smo_column_length = get_smo_length(period_1)


            return render(request, 'coordination_death_rebase.html', {'check_states' : check_states,
                                                                            'first_period' :period_1,
                                                                             'names' : names,
                                                                            'smo_column_length' : smo_column_length,
                                                                            'date_to_show' : get_date_to_show(self.dateYear1, self.dateMonth1)})

    def view_coordination_death(self, request, *args):
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
            self.set_all_data(data)
            d_reader = DataReader()
            all_smo = d_reader.load_model_smo_names()
            all_mo = d_reader.load_model_mo_names()
            if self.selectedSmo and self.selectedMo:
                if args:
                    data = self.filter_data(data, 'birthDate', gt=calculate_date(args)[0], lt=calculate_date(args)[1])
                names = self.get_names_list()
                daterange = get_daterange(self.dateYear1, self.dateMonth1)
                data = self.filter_data(data, 'smo_id', cond = self.selectedSmo)
                self.query = self.filter_data(data, 'endDate', gt=daterange[0], lt=daterange[1] )
                self.query = self.filter_data(self.query, 'result', cond=self.death_list)
                first_data_death = self.convert_data()
                daterange = get_daterange(self.dateYear2, self.dateMonth2)
                self.query = self.filter_data(data, 'endDate', gt=daterange[0], lt=daterange[1])
                self.query = self.filter_data(self.query, 'result', cond=self.death_list)
                second_data_death = self.convert_data( )
                output_data = self.return_data(first_data_death, second_data_death)
            return render(request, 'coordination_death.html', {   'smo_data'   : all_smo,
                                                                'mo_data'      : all_mo,
                                                                'names_list'   : names,
                                                                'data'         : output_data,
                                                                'month_year_1' : get_data_to_result_header(self.dateMonth1, self.dateYear1),
                                                                'month_year_2' : get_data_to_result_header(self.dateMonth2, self.dateYear2)})

    def view_coordination_death_load_classes(self, request, *args):
        u"""
        Вьюха, возвращающая позиции словаря по смо, мо
        :param request:
        :param args:
        :return:
        """
        if request.method == 'GET':
            mo=request.GET.get('mo', None)
            smo=request.GET.get('smo', None)
            month = request.GET.get('month', None)
            year = request.GET.get('year', None)
            if self.loadedData_year != year and self.loadedData_month != month:
                if self.load_monthly_report_data(month, year, is_death=True):
                    dataset = self.loadedData
                else:
                    dataset = None
            else:
                dataset = self.loadedData
            response_dict = dataset[int(smo)][int(mo)]

            return JsonResponse(response_dict)

    def view_coordination_death_load_blocks(self, request, *args):
        u"""
        Вьюха, возвращающая позиции словаря по смо, мо, нозологической форме
        :param request:
        :param args:
        :return:
        """
        if request.method == 'GET':
            mo=request.GET.get('mo', None)
            smo=request.GET.get('smo', None)
            month = request.GET.get('month', None)
            year = request.GET.get('year', None)
            classname = request.GET.get('classname', None)
            nos_data = self.get_blockname_data(smo, mo, year, month, classname,  dataframe=self.class_all_data, is_death=True)
            response_dict = nos_data

            return JsonResponse(response_dict)


class Reports_views(CoordinationBase):
    class_all_data = pd.read_csv('data/all_cases', index_col=0, parse_dates=True).rename(
                            columns={'caseZid__zap_id__smo_id': 'smo_id',
                                     'caseZid__lpu': 'lpu',
                                     'caseZid__stat_or_amb': 'stat_or_amb',
                                     'mkbExtra': 'mkb',
                                     'caseZid__dateBeg': 'begDate',
                                     'caseZid__dateEnd': 'endDate',
                                     'caseZid__result': 'result',
                                     'caseZid__zap_id__date_birth': 'birthDate',
                                     'caseZid__for_pom' : 'for_pom',
                                     'goalId' : 'goal_id'})

    def __init__(self):
        self._all_data = None
        super(CoordinationBase).__init__()

    def view_report_menu(self, request, *args):
        return HttpResponse('it works!')

    def view_report(self, request, *args):
        u"""

        :param request:
        :param args:
        :return:
        """
        self._all_data = self.class_all_data
        if args and args[0].startswith('d'):
            is_death_report = True
        else:
            is_death_report = False
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        if is_death_report:
            daterange = get_daterange(year, month)
            death_list = [105, 106, 205, 206, 313, 405, 406, 411]
            birth_filter = self.filter_data(self._all_data, 'birthDate', gt=calculate_date(args)[0], lt=calculate_date(args)[1])
            end_filter = self.filter_data(birth_filter, 'result', cond=death_list)
            first_period = self.filter_data(end_filter, 'begDate', gt=daterange[0], lt=daterange[1])
            slice_amb = self.filter_data(first_period, 'stat_or_amb', cond=3)
            slice_stat = self.filter_data(first_period, 'stat_or_amb', cond=[1, 2])
            slice_statzam = first_period[first_period.stat_or_amb.isna()]
            slice_skormp = self.filter_data(first_period, 'stat_or_amb', cond=4)
            nosologies = DataReader().get_nosologies()

            sum_amb = 0
            sum_stat = 0
            sum_statzam = 0
            sum_skormp = 0
            report_data = []
            for pos in nosologies:
                row = [0 for i in range(7)]
                row[0] = pos.number
                row[1] = pos.name
                row[2] = pos.mkbFirst if pos.mkbFirst == pos.mkbLast else pos.mkbFirst  + '-' + pos.mkbLast
                row[3] = len(self.filter_data(slice_amb, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[4] = len(self.filter_data(slice_stat, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[5] = len(self.filter_data(slice_statzam, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[6] = len(self.filter_data(slice_skormp, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                if len(pos.number) == 1:
                    sum_amb += row[3]
                    sum_stat += row[4]
                    sum_statzam += row[5]
                    sum_skormp += row[6]
                report_data.append(row)
            row = [0 for i in range(7)]
            row[0] = '6'
            row[1] = 'Итого'
            row[2] = 'Все случаи'
            row[3] = sum_amb
            row[4] = sum_stat
            row[5] = sum_statzam
            row[6] = sum_skormp
            report_data.append(row)
        else:
            daterange = get_daterange(year, month)
            birth_filter = self.filter_data(self._all_data, 'birthDate', gt=calculate_date(args)[0],
                                            lt=calculate_date(args)[1])
            first_period = self.filter_data(birth_filter, 'begDate', gt=daterange[0], lt=daterange[1])
            slice_amb = self.filter_data(first_period, 'stat_or_amb', cond=3)
            slice_amb_obr = self.filter_data(slice_amb, 'goal_id', cond='1.0')
            slice_amb_pos = self.filter_data(slice_amb, 'goal_id', cond='3.0')
            slice_stat = self.filter_data(first_period, 'stat_or_amb', cond=[1, 2])
            slice_stat_plan = self.filter_data(slice_stat, 'for_pom', cond='3')
            slice_stat_extr = self.filter_data(slice_stat, 'for_pom', cond=['1', '2'])
            slice_statzam = first_period[first_period.stat_or_amb.isna()]
            slice_skormp = self.filter_data(first_period, 'stat_or_amb', cond=4)
            nosologies = DataReader().get_nosologies()

            sum_amb_obr = 0
            sum_amb_pos = 0
            sum_stat_plan = 0
            sum_stat_extr = 0
            sum_statzam = 0
            sum_skormp = 0
            report_data = []
            for pos in nosologies:
                row = [0 for i in range(9)]
                row[0] = pos.number
                row[1] = pos.name
                row[2] = pos.mkbFirst if pos.mkbFirst == pos.mkbLast else pos.mkbFirst + '-' + pos.mkbLast
                row[3] = len(self.filter_data(slice_amb_obr, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[4] = len(self.filter_data(slice_amb_pos, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[5] = len(self.filter_data(slice_stat_plan, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[6] = len(self.filter_data(slice_stat_extr, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[7] = len(self.filter_data(slice_statzam, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                row[8] = len(self.filter_data(slice_skormp, 'mkb', gt=pos.mkbFirst, l=set_mkb_to_finder(pos.mkbLast)))
                if len(pos.number) == 1:
                    sum_amb_obr += row[3]
                    sum_amb_pos += row[4]
                    sum_stat_plan += row[5]
                    sum_stat_extr += row[6]
                    sum_statzam += row[7]
                    sum_skormp += row[8]
                report_data.append(row)
            row = [0 for i in range(9)]
            row[0] = '6'
            row[1] = 'Итого'
            row[2] = 'Все случаи'
            row[3] = sum_amb_obr
            row[4] = sum_amb_pos
            row[5] = sum_stat_plan
            row[6] = sum_stat_extr
            row[7] = sum_statzam
            row[8] = sum_skormp
            report_data.append(row)

        return render(request, 'report_base.html', {'data' : report_data,
                                                    'is_death_report' : is_death_report})