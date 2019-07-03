# -*- coding: utf-8 -*-
import os
import io
import xml.etree.cElementTree as ET

file_path = r'C:/Users/ivank/'

class Exchange(object):
    def __init__(self, file_path, month, year):
        self.month = month
        self.year = year
        self.file_name = '333'
        self.month = month
        self.year = year
        self.construct_file()

    def construct_file(self):
        Header = ET.Element('MR_OB')
        Header_ZGLV = ET.SubElement(Header, 'ZGLV')
        Header_SVD = ET.SubElement(Header, 'SVD')
        Header_OB_SV = ET.SubElement(Header, 'OB_SV')
        Header_PODR = ET.SubElement(Header, 'PODR')
        self.add_content_to_ZGLV(Header_ZGLV, filename=self.file_name, correction=True)

        self.add_content_to_SVD(Header_SVD)
        it_sv = self.add_content_to_OB_SV(Header_OB_SV)
        vzs_it = self.add_content_to_IT_SV(it_sv, 1)
        self.add_content_to_VZS_IT(vzs_it, 1, self.get_result)
        zap = self.add_content_to_PODR(Header_PODR)
        patient, case = self.add_content_to_ZAP(zap, 2, 3)
        self.add_content_to_PACIENT(patient, 2)
        self.add_content_to_SLUCH(case, 3, {3 : 'A00'})

        tree = ET.ElementTree(Header)
        tree.write('output_ekmp.xml', encoding='Windows-1251')

    def add_content_to_ZGLV(self, pref, filename=None, correction=None):
        ET.SubElement(pref, 'VERSION').text = '"3.0"'
        ET.SubElement(pref, 'DATA').text = '2019-06-30'
        ET.SubElement(pref, 'FILENAME').text = filename
        if correction:
            ET.SubElement(pref, 'FIRSTNAME').text = filename

    def add_content_to_SVD(self, pref):
        ET.SubElement(pref, 'CODE').text = ''
        ET.SubElement(pref, 'YEAR').text = '2019'
        ET.SubElement(pref, 'MONTH').text = '6'

    def add_content_to_OB_SV(self, pref):
        return ET.SubElement(pref, 'IT_SV')

    def add_content_to_IT_SV(self, pref, usl_ok):
        ET.SubElement(pref, 'N_SV').text = '1'
        ET.SubElement(pref, 'USL_OK').text = str(usl_ok)
        if usl_ok == 1:
            ET.SubElement(pref, 'FOR_POM').text = ''
        if usl_ok == 3:
            ET.SubElement(pref, 'AP_TYPE').text = ''
        return ET.SubElement(pref, 'VZS_IT')

    def add_content_to_VZS_IT(self, pref, age_group, result):

        ET.SubElement(pref, 'VZST'). text = str(age_group)
        ET.SubElement(pref, 'OT_NAIM').text = ''
        ET.SubElement(pref, 'ZBL_IT').text = '1243'
        ET.SubElement(pref, 'SMR_IT').text = '10'

    def add_content_to_PODR(self, pref):
        return ET.SubElement(pref, 'ZAP')

    def add_content_to_ZAP(self, pref, pacient, case):
        ET.SubElement(pref, 'N_ZAP').text = '3'
        pacient_xml = ET.SubElement(pref, 'PACIENT', attrib={'text': str(pacient)})
        case_xml = ET.SubElement(pref, 'SLUCH', attrib={'text' : str(case)})
        return pacient_xml, case_xml


    def add_content_to_PACIENT(self, pref, pacient_id):
        ET.SubElement(pref, 'DR').text = '1900-01-01'

    def add_content_to_SLUCH(self, pref, case_id, mkb):

        ET.SubElement(pref, "DATE_1").text = '2000-01-01'
        ET.SubElement(pref, 'DS1').text = mkb[case_id]
        ET.SubElement(pref, 'RSLT').text = ''
        ET.SubElement(pref, 'FOR_POM').text = ''
        ET.SubElement(pref, 'AP_TYPE').text = ''

    def create_file_if_not_exists(self, file_path):
        self.set_file_name()
        abs_path = file_path + self.file_name
        _bool = os.path.exists(abs_path)

        if not _bool:
            with io.open(abs_path, 'a+') as f:
                pass


    def get_result(self, age, is_death=None):
        return age

    def set_file_name(self):
        self.file_name = self.month + '-' + self.year

class Exchange_EKMP(object):
    def __init__(self, file_path, month, year):
        self.month = month
        self.year = year
        self.file_name = '333'
        self.month = month
        self.year = year
        self.construct_file()

    def construct_file(self):
        Header = ET.Element('MR_OB')
        Header_ZGLV = ET.SubElement(Header, 'ZGLV')
        Header_SVD = ET.SubElement(Header, 'SVD')
        Header_PODR = ET.SubElement(Header, 'PODR')
        self.add_content_to_ZGLV(Header_ZGLV, filename=self.file_name, correction=True)
        self.add_content_to_SVD(Header_SVD)
        zap = self.add_content_to_PODR(Header_PODR)
        patient, case, ekmp = self.add_content_to_ZAP(zap, 2, 3)
        self.add_content_to_PACIENT(patient, 2)
        self.add_content_to_SLUCH(case, 3, {3 : 'A00'})
        self.add_content_to_EKMP(ekmp, 0)

        tree = ET.ElementTree(Header)
        tree.write('output.xml', encoding='Windows-1251')

    def add_content_to_ZGLV(self, pref, filename=None, correction=None):
        ET.SubElement(pref, 'VERSION').text = '"3.0"'
        ET.SubElement(pref, 'DATA').text = '2019-06-30'
        ET.SubElement(pref, 'FILENAME').text = filename
        if correction:
            ET.SubElement(pref, 'FIRSTNAME').text = filename

    def add_content_to_SVD(self, pref):
        ET.SubElement(pref, 'CODE').text = ''
        ET.SubElement(pref, 'YEAR').text = '2019'
        ET.SubElement(pref, 'MONTH').text = '6'

    def add_content_to_OB_SV(self, pref):
        return ET.SubElement(pref, 'IT_SV')

    def add_content_to_IT_SV(self, pref, usl_ok):
        ET.SubElement(pref, 'N_SV').text = '1'
        ET.SubElement(pref, 'USL_OK').text = str(usl_ok)
        if usl_ok == 1:
            ET.SubElement(pref, 'FOR_POM').text = ''
        if usl_ok == 3:
            ET.SubElement(pref, 'AP_TYPE').text = ''
        return ET.SubElement(pref, 'VZS_IT')

    def add_content_to_VZS_IT(self, pref, age_group, result):

        ET.SubElement(pref, 'VZST'). text = str(age_group)
        ET.SubElement(pref, 'OT_NAIM').text = ''
        ET.SubElement(pref, 'ZBL_IT').text = '1243'
        ET.SubElement(pref, 'SMR_IT').text = '10'

    def add_content_to_PODR(self, pref):
        return ET.SubElement(pref, 'ZAP')

    def add_content_to_ZAP(self, pref, pacient, case, ekmp=True, no_ekmp=False):
        ET.SubElement(pref, 'N_ZAP').text = '3'
        pacient_xml = ET.SubElement(pref, 'PACIENT', attrib={'text': str(pacient)})
        case_xml = ET.SubElement(pref, 'SLUCH', attrib={'text' : str(case)})
        if ekmp: ekmp_xml = ET.SubElement(pref, 'EKMP', attrib={'text': 'true'})
        if no_ekmp: ET.SubElement(pref, 'NO_EKMP').text = '1'
        return pacient_xml, case_xml


    def add_content_to_PACIENT(self, pref, pacient_id):
        ET.SubElement(pref, 'DR').text = '1900-01-01'

    def add_content_to_SLUCH(self, pref, case_id, mkb):

        ET.SubElement(pref, "DATE_1").text = '2000-01-01'
        ET.SubElement(pref, 'DS1').text = mkb[case_id]
        ET.SubElement(pref, 'RSLT').text = ''
        ET.SubElement(pref, 'FOR_POM').text = ''
        ET.SubElement(pref, 'AP_TYPE').text = ''

    def add_content_to_EKMP(self, pref, ekmp_type, penalty=None):

        if penalty: ET.SubElement(pref, 'PROBLEM').text = penalty
        ET.SubElement(pref, 'TYPE').text = str(ekmp_type)
        if not penalty: ET.SubElement(pref, 'NO_PROBLEM').text = '1'

    def create_file_if_not_exists(self, file_path):
        self.set_file_name()
        abs_path = file_path + self.file_name
        _bool = os.path.exists(abs_path)

        if not _bool:
            with io.open(abs_path, 'a+') as f:
                pass


    def get_result(self, age, is_death=None):
        return age

    def set_file_name(self):
        self.file_name = self.month + '-' + self.year

if __name__ == "__main__":
    s = Exchange(file_path, '01', '2009')