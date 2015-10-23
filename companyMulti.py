# -*- coding: utf-8 -*-
'''
Created on 2015年10月18日
@author: Starmerx-001
'''
import gzip
import logging
import multiprocessing
import os
import random
import re
import sys
import time
import urllib2


reload(sys)
sys.setdefaultencoding("utf-8")

reLogin = "1688/淘宝会员登录"
reSalesRank = r"成交[\s]*?<span class=\"booked-count\">\s*?(.*?)\s*?<[\S\s]*?wp_widget_salesrank_side_title\"[\s]*?title=\"(.*?)\""
reAddress = r"地址：([\S\s]*?)<"
reAddress2 = r"址[\S\s]*?address[\S\s]*?>([\S\s]*?)<"

SLEEP_TIME = input("睡眠时间：") 

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s %(asctime)s] %(message)s',)


def readCategoryFile(categoryFile):
    result = {}
    try:
        with open(categoryFile, 'r') as fr:
            line = fr.readline()
            while line:
                temp = line.strip().split('\t')
                result[temp[0]] = temp[1]
                line = fr.readline()
        fr.close()    
    except Exception, e:
        logging.debug("%s]readCategoryFile()发生错误：%s" , multiprocessing.current_process().name, e)
    return result

def sleepTime(startTime, seconds):
    while time.time() - startTime < seconds:
        time.sleep(0.1) 

def creatHead():
    '''
    功能：创建一个HTTP的头部信息。
    @param 无 
    @return: 返回一个字典变量。
    '''
    cacheControl = ['max-age=0', 'no-cache']
    connection = ['keep-alive', 'closed']
    userAgent = ['Mozilla/5.0 (X11; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0',
                 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
                 'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0']
#    host = ['s.1688.com', 'www.1688.com']
    referer = ['www.baidu.com', 's.1688.com', 'www.1688.com', 'www.hao123.com', 'www.sogou.com',
               'www.google.com.hk', 'cn.bing.com', 'www.yahoo.com']
    cookie = 'JSESSIONID=8L782Iqv1-4hOUlqWY5Zr8ft3RZB-ag1SYPP-WT91;\
            _tmp_ck_0="O3HdOLdLuB%2FZTCy2B%2Fu7mSJdIjVfWWS6YDwxz%2BRH7hXpwerJneOxVJMSGb1dkZ7krs4MepLSU09ni3SyesPgNVtqmOyA6zq3Qf5LkeiLgJmS8t%2FUEcANzX5CfBQRHl2wl3%2BO0Ne2upCtdLixL5JF5youIP%2B%2B4hUCskR%2FkwU%2FVY74ERUjA%2Flmkxx4cWAaMr1Jh%2FmpcDWdxyp%2FUCOVXKSZXsIU72uT8ZbQbN6ZDO4P9OOqzPphi0PLzFGk5qTC3ng2MFWIKQGNvIJwpKnileqGPsAn7c418HkVXJ8cfzHv9KDpLn0VScMlw9UvB4eNtWUAJy%2ByyeDQQU1Rzq59YrPJ3qq%2BBR1PdCbS0K%2FHI%2FG7LWW9doRomYyF0yPm6CYZ%2BQO7G8qxCzI7Tuk%3D";\
            __cn_logon__=false;\
            cna=9yxYDhvlYjgCAbftRGYjtFi9;\
            isg=D84F35D067965ED78035192854B07F48;\
            l=AsbGrB77/Z/kDu414F800QOGNrZIJwrh;\
            ali_beacon_id=[ip].[time].087825.2;\
            ali_ab=[ip].[time].3;\
            alisw=swIs1200%3D1%7C;\
            alicnweb=touch_tb_at%3D[time]'
            
    ip = str(random.randint(1, 254)) + "." + str(random.randint(1, 254)) + "." + str(random.randint(1, 254)) + "." + str(random.randint(1, 254))
    nowTime = str(int(time.time()))
    
    head = {}
    head['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    head['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    head['Cache-Control'] = cacheControl[random.randint(0, len(cacheControl) - 1)]
    head['Connection'] = connection[random.randint(0, len(connection) - 1)]
#    head['Host'] = host[0]
    head['User-Agent'] = userAgent[random.randint(0, len(connection) - 1)]
    head['Referer'] = referer[random.randint(0, len(referer) - 1)]
    head['Cookie'] = cookie.replace("[ip]", ip).replace("[time]", nowTime)

    return head

def getCompanyInfo(company):
    companyURL = company[0]
    addressURL = companyURL + '/page/contactinfo.htm'
    sales = u''
    address = u'地址：'
    flg = False
    try:
        startTime = time.time()
        req = urllib2.Request(addressURL, headers=creatHead())
        html = urllib2.urlopen(req).read() 
        htmlNew = html.decode('gbk').encode("utf-8")
        temp = re.findall(reAddress, htmlNew)     
        if temp:
            flg = True
            address = address + unicode(temp[0].strip())
            with gzip.open("./1688/" + categoryId + "/" + company[2] + "_address.html.gz", 'w') as fw1:
                fw1.write(html)
                fw1.close()
            sleepTime(startTime, SLEEP_TIME)
        else:
            htmlNew = html.decode("gbk").encode("utf8")
            if htmlNew.find("1688/淘宝会员登录") != -1:
                logging.debug("%s] 登陆...%s" , multiprocessing.current_process().name, addressURL)
                sleepTime(startTime, random.randint(30, 180))
            else:
                logging.debug("%s]第一种正则表达式没有找到地址！%s", addressURL)
                temp = re.findall(reAddress2, htmlNew)
                if temp:
                    flg = True
                    address = address + unicode(temp[0].strip())
                    with gzip.open("./1688/" + categoryId + "/" + company[2] + "_address.html.gz", 'w') as fw1:
                        fw1.write(html)
                        fw1.close()
                    sleepTime(startTime, SLEEP_TIME)
                else:
                    htmlNew = html.decode("gbk").encode("utf8")
                    if htmlNew.find("1688/淘宝会员登录") != -1:
                        logging.debug("%s] 登陆...%s" , multiprocessing.current_process().name, addressURL)
                        sleepTime(startTime, random.randint(30, 180))
                    else:
                        logging.debug("%s]第二种正则表达式没有找到地址！%s", addressURL)    
                        
            startTime = time.time()        
            req = urllib2.Request(companyURL, headers=creatHead())
            html = urllib2.urlopen(req).read() 
            htmlNew = html.decode('gbk').encode("utf-8")   
        
        temp = re.findall(reSalesRank, htmlNew)     
        if temp:
            for item in temp:
                sales = sales + unicode(item[1] + u'：成交' + unicode(item[0].strip()) + u'笔\t')
            with gzip.open("./1688/" + categoryId + "/" + company[2] + ".html.gz", 'w') as fw2:
                fw2.write(html)
                fw2.close()
            sleepTime(startTime, SLEEP_TIME)
        else:
            htmlNew = html.decode("gbk").encode("utf8")
            if htmlNew.find("1688/淘宝会员登录") != -1:
                logging.debug("%s] 登陆...%s" , multiprocessing.current_process().name, companyURL)
                sleepTime(startTime, random.randint(30, 180))
            else:
                logging.debug("%s]没有销售排行！%s", multiprocessing.current_process().name, companyURL)
                 
    except Exception, e:
        logging.debug("%s]getCompanyURL()发生%s错误:%s", multiprocessing.current_process().name, e, companyURL)
    
    if flg: 
        logging.debug("%s]%s %s\t销售：%d 地址：%s", multiprocessing.current_process().name, companyURL, company[2], len(temp), address)   
        with open("./result/" + categoryId + '.csv', 'a')as fw:
            fw.write(unicode(company[2]) + u',' + unicode(companyURL) + u',' + unicode(address) + u',' + unicode(company[1]) + u',' + unicode(sales) + u'\n')
            fw.close()

if __name__ == '__main__':
    logging.debug("%s]%s\t程序开始运行：%s", multiprocessing.current_process().name, os.path.basename(__file__), time.strftime("%Y-%m-%d %X"))
    if not os.path.exists('./result'):
        os.mkdir('./result')
    if not os.path.exists('./1688'):
        os.mkdir('./1688')
    beginTime = time.time()
    categorys = readCategoryFile("./data/category_have.log")

    for item in categorys:
        categoryId = item[28:].replace('-', '').replace('.html', '')
        logging.debug("%s 类：%s", categorys[item], categoryId)
        if os.path.exists("./result/company/" + categoryId + "_company.csv"): 
            companyList = []
            companyHave = {} 
            if os.path.exists("./result/" + categoryId + '.csv'):
                with open("./result/" + categoryId + '.csv', 'r')as frh:
                    line = frh.readline()
                    while line:
                        temp = line.strip().split(',')
                        companyHave[temp[1]] = 1
                        line = frh.readline()
            with open("./result/company/" + categoryId + "_company.csv", 'r')as fr:
                line = fr.readline()
                while line:
                    temp = line.strip().split(',')
                    if not companyHave.has_key(temp[0]):
                        companyList.append(temp)
                    line = fr.readline()
            
            if not os.path.exists('./1688/' + categoryId):
                os.mkdir('./1688/' + categoryId)
            pool = multiprocessing.Pool(multiprocessing.cpu_count() * 5 - 1)
            offerIdList = pool.map(getCompanyInfo, companyList)
            pool.close()
            pool.join()
    endTime = time.time()
    logging.debug("%s]程序运行结束：%s", multiprocessing.current_process().name, time.strftime("%Y-%m-%d %X"))
    logging.debug("%s]用时：%f", multiprocessing.current_process().name, endTime - beginTime)
    pass
