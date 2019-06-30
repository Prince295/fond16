import requests

START_DATE = '2015-1-01'
STOP_DATE = '2019-6-01'

def load_site_data(start, stop, is_illness=False, is_death=False):
    year_start, month_start, day_start = start.split('-')
    year_stop, month_stop, day_stop = stop.split('-')
    if is_illness:
        query_year = year_start
        query_month = month_start
        while int(year_stop) > int(query_year) or int(month_stop) > int(query_month):
            try:
                response = requests.get('http://localhost:8000/coordination_illness_rebase/'
                                        '?selected_smo=&selected_mo=&selected_year_1={year}'
                                        '&selected_month_1={month}&checkbox_percent=false'
                                        '&checkboxDownload=false&colorDiff=false'.format(year=query_year, month=query_month))
                print('ready {} year, {} month'. format(query_year, query_month))
            except requests.exceptions.ConnectTimeout:
                print('timeout')

            print(query_month + ' ' + query_year)
            query_month = int(query_month) + 1
            if query_month > 12:
                query_month = 1
                query_year = int(query_year) + 1
            query_month = str(query_month)
            query_year = str(query_year)
    if is_death:
        query_year = year_start
        query_month = month_start
        while int(year_stop) > int(query_year) or int(month_stop) > int(query_month):
            try:
                response = requests.get('http://localhost:8000/coordination_death_rebase/'
                                        '?selected_smo=&selected_mo=&selected_year_1={year}'
                                        '&selected_month_1={month}&checkbox_percent=false'
                                        '&checkboxDownload=false&colorDiff=false'.format(year=query_year,
                                                                                         month=query_month))
                print('ready {} year, {} month'.format(query_year, query_month))
            except requests.exceptions.ConnectTimeout:
                print('timeout')

            print(query_month + ' ' + query_year)
            query_month = int(query_month) + 1
            if query_month > 12:
                query_month = 1
                query_year = int(query_year) + 1
            query_month = str(query_month)
            query_year = str(query_year)


if __name__ == '__main__':
    load_site_data(START_DATE, STOP_DATE, True, True)

