# -*- coding: utf-8 -*-
__author__ = 'songtao'



import re,json
import urllib2
from pandas import DataFrame,Series
import pandas as pd


# requests.get

# 处理字符串的函数
def ProcessingString(string):
    string = string.encode('utf-8')
    string = str(string).replace(r'\x','%').replace(r"'","")
    string = re.sub('^b','',string)
    return string

# 计算总共页数
def SearchPageCount(position, city):
    i = 0
    type = 'true'
    url = 'http://www.lagou.com/jobs/positionAjax.json?city='+city+'&first='+type+'&kd='+position+'&pn='+str(i+1)
    f = urllib2.urlopen(url)
    data = f.read()
    count = int(json.loads(str(data))["content"]["totalPageCount"])
    totalCount = int(json.loads(str(data))["content"]["totalCount"])
    print('本次搜索到%d个职位'%totalCount)
    return count

def LaGouSpiderWithKeyWord(position, city):
    positionTemp = ProcessingString(position)
    cityTemp = ProcessingString(city)
    # 获取总共页数
    pageCount = SearchPageCount(positionTemp,cityTemp)

    for i in range(0,pageCount):
        if i ==0 :
            type='true'
        else:
            type='false'
        url = 'http://www.lagou.com/jobs/positionAjax.json?city='+cityTemp+'&first='+type+'&kd='+positionTemp+'&pn='+str(i+1)
        data = urllib2.urlopen(url).read()
        #     读取Json数据
        jsondata = json.loads(str(data))['content']['result']
        for t in list(range(len(jsondata))):
            jsondata[t]['companyLabelListTotal']='-'.join(jsondata[t]['companyLabelList'])
            jsondata[t].pop('companyLabelList')
            if t == 0:
                rdata=DataFrame(Series(data=jsondata[t])).T
            else:
                rdata=pd.concat([rdata,DataFrame(Series(data=jsondata[t])).T])
        if i == 0:
            totaldata=rdata
        else:
            totaldata=pd.concat([totaldata,rdata])
        print('正在解析第%d页...'%i)
        xls = 'lagou'+position+'.xls'
        totaldata.to_excel(xls,sheet_name='sheet1')


if __name__ == "__main__":
    position = u'土木工程师'
    city = u'北京'
    LaGouSpiderWithKeyWord(position, city)
