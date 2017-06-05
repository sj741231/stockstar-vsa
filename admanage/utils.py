# -*- coding: utf-8 -*-
__author__ = 'songtao'

from .models import GroupReleation
import xlrd

def uploadgrouprelation(xlsfile):
    GroupReleation.objects.all().delete()
    data = xlrd.open_workbook(xlsfile)
    table = data.sheet_by_name("Sheet1")
    rows = table.nrows
    fail_list = []
    for i in range(1, rows):
        row_value = table.row_values(i)
        # adtree,attchto,department,company = row_value
        if GroupReleation.objects.filter(adtree=row_value[0]):
            GroupReleation.objects.filter(adtree=row_value[0]).update(**{'attachto':row_value[1],'department':row_value[2],'company':row_value[3]})
        else:
            GroupReleation.objects.create(**{'adtree':row_value[0],'attachto':row_value[1],'department':row_value[2],'company':row_value[3]})

