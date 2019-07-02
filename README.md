# fond16
## Краткие сведения по установке

версия python 3.x (пробовал на 3.6.5 и 3.7.1)

1. Клонируем репозиторий
2. Качаем коннектор оракла под винду или линукс, распаковываем, добавляем папку с коннектором в пути
3. Внутри проекта лежит файлик requirements.txt - устанавливаем все библиотеки
4. в папке с проектом разворачиваем python3 manage.py runserver 0.0.0.0:8000 & (развернет процесс в UNIX в качестве фонового - для теста сойдет)
5. так как кэш локальный - некоторые отчеты могут довольно долго грузиться ( что с этим сделать - после запуска сервера по разу прогрузить все отчеты, они сохранятся в локальном кэше и будут живенько грузиться. В релизной версии конечно же будет пофикшено) 


## Что можно показать
1. Сервис поручений сыроват - там почти ничего нет, просто пример, как это будет выглядеть. Форма будет похожа на ту, что в тз
2. Координационный совет сейчас выдает по заболеваниям - очень похожую на аналитическую форму (разница только в том, что у меня нет разделения по посещениям ( будет, тут данные и понимание есть, как это сделать) 
3. Координационный совет по смертности - выдает печатную форму, на нее будет список смо и мо как в заболеваемости и будет форма, как заказывали, то есть сейчас это отдельные отчетики без фильтров по мо, для наглядности (одни нули показывать такое себе)) 
4. Таблица поручений - по тз должна заполняться чуть ли не от руки (выгрузка показателей) 
5. Контроль поручений - должны подгружаться практические показатели и нормы, заполненные от руки и должен быть результат сравнения этих показателей - собственно у меня практические подгружаются ( почти клон таблицы поручений с бэкслешами и ноликами) )
6. В целом, ссылки все рабочие ( может где роуты не совсем верные, но все будет ) - тыкать можно везде и тд.

## ToDo List
#### 1. Поручения:
- Модели Orders, Orders_OrderTable, OrderTable
- Таблицы в TFOMS_DATA: ORDERS(id, datetime, person_id(fk_user), text, status ), ORDERTABLE(id, order_id(fk_order)), ORDERTABLE_RECORD(id, mo_id(fk_F003), ks, smp, amp,  ordertable_id(fk_ordertable),  nos_id(fk_NSLGS))
- Роут для записи  @создание поручения
- Роуты для редактирования, удаления (для подтвержденных поручений нет возможности редактирования и удаления) @все поручения
- Вывод поручения на печать, экспорт в doc, docx - можно совместить
- На данный момент нет разделения по правам групп пользователей (пока разделение на авторизованных и неавторизованных)
- Метод для отбора необходимых для контроля МО (брать из 107 формы - отбирать "красные" случаи - те, у которых более 10% положительной динамики по отношению к предыдущему месяцу или(и) предыдущему году). На основе этих данных будет формироваться таблица в @Поручения -> Таблица, а также в @Поручения -> Контроль. Переписать это все красиво в отдельный класс. Предусмотреть обработку параметра - id поручения, id таблицы
- Проверить метод load_data_old во views (скорее всего имеет смысл переписать его по аналогии со 107 формой (брать данные из df, а не из базы, также имеет смысл избавиться от глобальных переменных: лучше всего сделать потомком CoordinationBase. Лпу брать из таблицы выше. Продумать хранение - имеет ли смысл долговременно хранить эти таблицы, или лучше собирать их в момент запроса) 
- Передавать во @все поручения список Поручений. В таблицы и контроль передавать список поручений и список таблиц для поручений.
- Внешний вид поручений и контроля поручений (обсуждаемо):
4. Нозологическая форма
4.1.Амбулаторно-поликлинической медицинской помощи, посещения
4.1.1. Обращения в связи с заболеванием
4.1.2. Разовое посещение в связи с заболеванием
4.2. Стационарной медицинской помощи, случай госпитализации
4.2.1. Плановая госпитализация
4.2.2. Экстренная госпитализация
4.3. Стационарозамещающей медицинской помощи, случай лечения
4.4. Скорой медицинской помощи вне медицинской организации, вызов
Описание строк:
Данные размещаются блоками. Блок СМО содержит все МО данной СМО. Блок МО содержит все нозологические формы данной МО (Идентичны для всех МО).
Алгоритм формирования данных в ячейке:
Для данной нозологической формы для данного МО выводится n/m. Где m — количество порученных экспертиз, а n — количество выполненных экспертиз. Ячейка подсвечивается красным, если n < m.

#### 2. 107:
- В любой момент работы с отчётной формой, из неё можно сделать печатную форму и вывести на печать. При этом, на печати будут те группировки и строки/столбцы, которые были выбраны. Предложение открывать в excel html файл. Более сложный вариант генерировать пдфку через условный weasyprint (не очень хочется этого делать).
- Можно выбрать произвольный отрезок периодов (март-сентябрь, к примеру) и тогда в п.5. будет сравнение количества периодов к предыдущему такому же количеству периодов (июнь-август к март-май), а в п.6. будет сравнение периодов к аналогичным периодам предыдущего года - тут добавить опциональный комбобокс, во вьюхе добавить опцию пересчета нужных периодов ( с подсчетом значений проблем быть не должно - просто суммировать значения словарей с данными )
- Выгрузка в файл ( так как выгрузка будет довольно долгой ( там по стандарту нужно выгружать не только циферки, но еще и случаи, входящие в эти циферки, что делает данную выгрузку ну очень мерзкой) возможно будет иметь смысл бросить ее в очередь с Celery).
При выгрузке необходимо заполнять поля по экспертизам. PROBLEM - брать из S_OSN таблицы SANKS. SANK_EKMP из SCHETS (связь с Z_SLS через таблицу ZAPS)
- Аналитика: Постараться врезать в html-ответ plotly html-файл
- Добавить подгрузку по диагнозам. Аналогично блокам
- Добавить вместе со сворачиваемостью/разворачиваемостью скрываемость. Также переделать скрываемость для шапок.
FRONT: в таблице в методе, который скрывает все мо для смо: либо создавать новый row, в котором будет клон элемента смо, либо в row с 'Итого' на 1 позицию вставлять элемент смо. в любом случае, красивого решения я пока не вижу.

#### 3. Выгрузка:
- Либо pandas.to_excel, либо способ из 107. 
- Добавить шапки в таблицы (во вьюхах отправлять месяц/год)

#### 4. 104
- Видоизменить формат нозологических форм. В таблицу добавить поля for_child, for_adult, for_pens. При выгрузке отчетов в формы учитывать значения этих полей. Также добисать названия отсутствующих нозологических форм и добавить заголовочные поля (хотя их можно не в базу, а просто отредактировать в отчете) 
