from django.db import models
from django.utils.timezone import now
# Create your models here.

class SLS(models.Model):
    caseZid = models.CharField(db_column='Z_SLID', max_length=16, blank=False, verbose_name='ID_случаев_Z')
    caseId = models.CharField(db_column='SL_ID', max_length=36, verbose_name="ID_случаев")
    lpuId = models.CharField(db_column='LPU_1', max_length=8, verbose_name="номер ЛПУ")
    unit = models.CharField(db_column='PODR', max_length=16, verbose_name="подразделение")
    profil = models.PositiveSmallIntegerField(db_column='PROFIL',verbose_name="профиль")
    profilK = models.PositiveSmallIntegerField(db_column='PROFIL_K', verbose_name="профиль койки")
    child = models.PositiveSmallIntegerField(db_column='DET', verbose_name='Дети')
    goalId = models.CharField(db_column='P_CEL', max_length=3, verbose_name='цель посещения')
    history = models.CharField(db_column='NHISTORY', max_length=50, verbose_name='история')
    period = models.PositiveSmallIntegerField(db_column='P_PER', verbose_name='период')
    dateBeg = models.DateTimeField(db_column='DATE_1', verbose_name='дата начала')
    dateEnd = models.DateTimeField(db_column='DATE_2', verbose_name='дата окончания')
    kd = models.IntegerField(db_column='KD', verbose_name='-----')
    mkb = models.CharField(db_column='DS0', max_length=10, verbose_name='МКБ')
    mkbExtra = models.CharField(db_column='DS1', max_length=10, verbose_name='МКБ-доп')
    mkbOnk = models.PositiveSmallIntegerField(db_column='DS_ONK', verbose_name='МКБ-онк')
    dn = models.PositiveSmallIntegerField(db_column='DN',verbose_name='---')
    mes = models.CharField(db_column='CODE_MES2', max_length=20, verbose_name='Код Мес')
    reabilitation = models.IntegerField(db_column='REAB', verbose_name='Реабилитация')
    prvs = models.IntegerField(db_column='PRVS', verbose_name='----')
    vers_spec = models.CharField(db_column='VERS_SPEC', max_length=4 ,verbose_name='--------')
    personId = models.CharField(db_column='IDDOKT', max_length=25, verbose_name='Лечащий врач')
    ed_col = models.DecimalField(db_column='ED_COL', max_digits=7, decimal_places=2, verbose_name='___')
    tariff = models.DecimalField(db_column='TARIF', max_digits=17, decimal_places=2, verbose_name='Тариф')
    price = models.DecimalField(db_column='SUM_M', max_digits=17, decimal_places=2, verbose_name='Сумма')
    comment = models.CharField(db_column='COMENTSL', max_length=250, verbose_name='Комментарий')
    vid_hmp = models.CharField(db_column='VID_HMP', max_length=12, verbose_name='-')
    metod_hmp = models.PositiveSmallIntegerField(db_column='METOD_HMP', verbose_name='-')
    ticket_date = models.DateField(db_column='TAL_D', verbose_name='Дата номерка')
    ticket_num = models.CharField(db_column='TAL_NUM', max_length=20, verbose_name='Номерок')
    ticket_end_date = models.DateField(db_column='TAL_P', verbose_name='Дата окончания номерка')
    pr_d_n = models.PositiveSmallIntegerField(db_column='PR_D_N', verbose_name='..')
    mkbEx = models.PositiveSmallIntegerField(db_column='DS1_PR', verbose_name='Предыдущий мкб')
    brokenCase = models.PositiveSmallIntegerField(db_column='PRERV_SLUCH', verbose_name='Прерванный случай')
    c_zab = models.PositiveSmallIntegerField(db_column='C_ZAB', verbose_name='...')

    class Meta:
        db_table='"SLS"'

class Nosologies(models.Model):
    number = models.DecimalField(db_column='NUMBER', max_digits=2, decimal_places=2, verbose_name='Номер')
    name = models.CharField(db_column='NAME', max_length=150, blank=False, verbose_name='Заболевание')
    mkbFirst = models.CharField(db_column='MKBFIRST', max_length=6, verbose_name='с_МКБ')
    mkbLast = models.CharField(db_column='MKBLAST', max_length=6, verbose_name='по_МКБ')

    class Meta:
        db_table='"NSLGS"'

class Patients(models.Model):
    client_id = models.CharField(db_column='ID_PAC', max_length=36, verbose_name='Айди пациента')
    date_birth = models.DateTimeField(db_column='DR', verbose_name='Дата рождения')

    class Meta:
        db_table='"PACIENTS"'

class Lpu_names(models.Model):
    lpu_id = models.BigIntegerField(db_column='MCOD', blank=False, verbose_name='Код ЛПУ')
    name_full = models.CharField(db_column='NAM_MOP', max_length=254, verbose_name='Название')
    name_short = models.CharField(db_column='NAM_MOK', max_length=254, verbose_name='Сокращенное название')
    address = models.CharField(db_column='ADDR_J', max_length=254, verbose_name='Адрес')
    is_deleted = models.PositiveSmallIntegerField(db_column='IS_DELETED', default=0, verbose_name='Удален')

    class Meta:
        db_table='"F003_LO"'






