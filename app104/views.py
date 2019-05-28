from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.conf import settings
from .models import SLS, Nosologies
from django.db.models import Count

global _data
_data = []

def load_data(request):
    nosologies = Nosologies.objects.all()
    lpu_list = []
    lpus = {1: 47007406,
            2: 47007405,
            3: 74}
    for k, v in lpus.items():
        lpu_list.append(SLS.objects.filter(lpuId=v).annotate(ds1count=Count(SLS.mkbExtra)))
        lpu_list.append(SLS.objects.filter(lpuId=v, goalId__in=['1.0', '1.1', '1.2', '1.3']).annotate(
            ds1count=Count(SLS.mkbExtra)))
        lpu_list.append(
            SLS.objects.filter(lpuId=v, goalId__in=['2.1', '2.2', '2.3', '2.5' '2.6', '3.0']).annotate(
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
    data, lpus = get_data()
    return render(request, 'index.html', {'data' : data,
                                          'lpus' : lpus
                                          })

def mo_views(request):
    data, lpus = get_data()


    return render(request, 'mo_views.html', {'data': data,
                                          'lpus': lpus
                                          })

def mo_views_table(request):
    u"""
    Данная вьюха выглядит максимально готовой( тут нужна только оптимизация разделения случаев на амбулаторные и стационарные
    """
    data, lpus = get_data()
    return render(request, 'mo_views_table.html', {'data' : data,
                                                   'lpus' : lpus})

def mo_views_ctrl_tbl(request):
    u"""
    Тут необходимо накладывать данные из таблицы выше
    и сравнивать их с ожидаемыми  (изменять заливку ячейки в случае различий)
    :param request:
    :return:
    """
    data, lpus = get_data()
    return render(request, 'mo_views_control_table.html', {'data' : data,
                                                           'lpus' : lpus})

def documents_base(request):
    return render(request, 'documents_base.html')

def documents_all(request):
    return render(request, 'documents_all.html')

def documents_new(request):
    return render(request, 'documents_new.html')

def coordination(request):
    data, lpus = get_data()

    return render(request, 'coordination.html', {'data': data,
                                             'lpus': lpus
                                             })

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

def get_data():
    u"""
    Универсальный метод подгрузки данных в формы.
    На тестовом образце таким простым образом реализовано кэширование(хранятся данные в списке
    _data
    :return: данные + список лпу( на данный момент нет списка организаций Лен. Области)
    """
    lpus = {1: 47007406,
            2: 47007405,
            3: 74}
    if _data:
        return _data, lpus
    else:
        nosologies = Nosologies.objects.all()
        lpu_list = []

        for k, v in lpus.items():
            lpu_list.append(SLS.objects.filter(lpuId=v).annotate(ds1count=Count(SLS.mkbExtra)))
            lpu_list.append(SLS.objects.filter(lpuId=v, goalId__in=['1.0', '1.1', '1.2', '1.3']).annotate(
                ds1count=Count(SLS.mkbExtra)))
            lpu_list.append(
                SLS.objects.filter(lpuId=v, goalId__in=['2.1', '2.2', '2.3', '2.5' '2.6', '3.0']).annotate(
                    ds1count=Count(SLS.mkbExtra)))
        row = [0 for j in range(len(lpu_list) + 5)]
        data = []
        for i, n in enumerate(nosologies):
            data.append([0 for j in range(len(lpu_list) + 5)])
            data[i][0] = n.number
            data[i][1] = n.name
            for num, lpu1 in enumerate(lpu_list):
                for lpu in lpu1:
                    if (n.mkbFirst <= lpu.mkbExtra) and (n.mkbLast >= lpu.mkbExtra):
                        data[i][num + 2] += lpu.ds1count
                        if num % 3 == 0:
                            data[i][len(row) - 3] += lpu.ds1count
                        elif num % 3 == 1:
                            data[i][len(row) - 2] += lpu.ds1count
                        else:
                            data[i][len(row) - 1] += lpu.ds1count

    return data, lpus



