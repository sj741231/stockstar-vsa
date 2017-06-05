# -*- coding: utf-8 -*-
'''
shijin 
'''
from collections import namedtuple
from warnings import catch_warnings
import xlrd, sys

reload(sys)  
sys.setdefaultencoding('utf8')   

print sys.getdefaultencoding()

class Opt_excel(object):
    
    def __init__(self):
        '''
        初始化参数：文件对象，标签页，表列，表行
        '''
        self._excel_file = None         #文件名
        self._ob_file = None            #xlrd文件对象
        self._excel_sheet = None        #标签页list
        self._columns = []              #表头字段list
        self._row = None                #
        
    
    def check_file(self,_excel_file):
        '''
        检查文件及标签页
        '''
        try:
            self._ob_file = xlrd.open_workbook(_excel_file)
            #print type(self._ob_file)
            self._excel_sheet = self._ob_file.sheet_names()
        except IOError:
            print ("％ 文件不存在或者打开错误" % (_excel_file))
         
        return self._ob_file
    
    
    def excel_sheets(self):
        '''
        返回excel标签页名字，list
        '''
        return self._excel_sheet
    
    
    def load_data(self,sheetname = None):
        '''
        1、判断是否有指定标签页，如果没有默认使用0标签页加载表
        2、或取标签页第一行字段名称,存入_columns
        3、循环输出表的数据
        '''
        if sheetname == None:
            table = self._ob_file.sheet_by_index(0)
        elif sheetname in _excel_sheet:
            table = self._ob_file.sheet_by_name(u'sheetname')
        else:
            raise ValueError
            
        self._columns = table.row_values(0)  #取表第一行，表头  #取表第一行，表头  table.row_values(1)
        listx1=[]
        print self._columns
        print str(self._columns).decode('unicode-escape')
        for x in self._columns:
            print x +' ',
           # listx1.append(x.encode('utf-8'))
            listx1.append(x.decode('unicode-escape'))
            print listx1
        print ''
        #for y in listx1:
        #    print "listx1: ",
        #    print y
        #print listx1
        print "----------------------------------------------------------"
        '''
        self._columns1 = table.row_values(1)  #取表第一行，表头
        print self._columns1
        print str(self._columns1).decode('unicode-escape')
        print "----------------------------------------------------------"
        
        list1 = zip(self._columns,self._columns1)
        print list1
        print "--------------------------------------"
        '''         
        #nm = namedtuple('nm',self._columns1)
        
       # self._row = table.row_values(1)  #取表第二行
        
        #aaa = nm._make(self._row)
        
        #print aaa
        
        #for x in nm:
        #    print str(x).decode('UTF-8') 
        
        
        '''
        for j in range(table.nrows):
            row_data = table.row_values(j)
            print tb_data._make(row_data)
        '''   
        return
        
        
        
    

if  __name__  == "__main__":
    print "this is use_excel test !"
    #print sys.argv[1]
    test = Opt_excel()
    test.check_file("/data/jump/vsa/admanage/sjtest11.26.xlsx")
    #print test.excel_sheets()
    test.load_data()
    
    
    #load_excel(sys.argv[1])
   