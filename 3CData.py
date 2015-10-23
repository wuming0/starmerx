# -*- coding: utf-8 -*-
'''
Created on 2015年10月17日
@author: Starmerx-001
'''
# -*- coding: utf-8 -*-
'''
Created on 2015年10月17日
@author: Starmerx-001
'''

import cookielib
import os
import random
import re
import sys
import time
import urllib2
import MySQLdb
from _mysql import DatabaseError
import chardet
import gzip

reload(sys)
sys.setdefaultencoding("utf-8")

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

reLogin = "1688/淘宝会员登录"
reOfferNum = r"共.*?<em>(.*?)</em>件相关产品"

reCompany = r"(sm-offer-trade.*?title=\"(.*?)\"[\S\s]*?)?memberid=\".*?href=\"(.*?)\".*?title=\"(.*?)\"[\S\s]*?sm-offer-location.*?title=\"(.*?)\""

reSalesRank = r"成交[\s]*?<span class=\"booked-count\">\s*?(.*?)\s*?<[\S\s]*?wp_widget_salesrank_side_title\"[\s]*?title=\"(.*?)\""
reAddress = r"地址：([\S\s]*?)<"

SLEEP_TIME = 3  # input("睡眠时间：") 
LIMIT_PAGE_NUMBER = 6000
ASYNC_COUNT = 100

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
        print "readOfferIdFile 发生错误：", e
    return result

def splitPrice(categoryURL):
    priceList = [0]
    numList = []
    try:
        total = offerNum = 1000000
        while offerNum > LIMIT_PAGE_NUMBER:
            startTime = time.time()
            priceStart = priceList[len(priceList) - 1]
            priceEnd = 3.4028235E38
            url = categoryURL + '?uniqfield=userid&priceStart=' + unicode(priceStart) + '&priceEnd=' + unicode(priceEnd)
            req = urllib2.Request(url, headers=creatHead())
            html = urllib2.urlopen(req).read()
            html = html.decode('gbk').encode("utf-8")
                    
            if html.find(reLogin) == -1:
                temp = re.search(reOfferNum, html)
                if temp:
                    offerNum = int(temp.group(1))
                    if priceStart == 0:
                        total = offerNum
                else:
                    print time.strftime("%F %X\t"), "找不到产品数目：", url
                    priceList.append(round(priceEnd, 2))
                    numList.append(0)
                    break
            else:
                print time.strftime("%F %X\t"), "登陆：", url
                sleepTime(time.time(), SLEEP_TIME * random.randint(12, 120))
                continue
            count = 0
            num = offerNum
            price = priceEnd
            
            if offerNum <= LIMIT_PAGE_NUMBER:
                priceList.append(round(priceEnd, 2))
                numList.append(offerNum)
                break
            
            if total == num:
                addPrice = 1.0
            else:
                addPrice = round(priceStart * LIMIT_PAGE_NUMBER / (total - num) * 5, 2)
                if num * 3 > total:
                    addPrice = round(addPrice / 3, 2)
                if num < 10 * LIMIT_PAGE_NUMBER:
                    addPrice = round(addPrice ** 2, 2)
            while num > LIMIT_PAGE_NUMBER and addPrice >= 0.01:
                price = round(priceStart, 2) + addPrice
                addPrice = round(addPrice / 2 - 0.0001, 2) 
                count = count + 1
                url = categoryURL + '?uniqfield=userid&priceStart=' + unicode(priceStart) + '&priceEnd=' + unicode(priceEnd)
                
                sleepTime(startTime, SLEEP_TIME)
                startTime = time.time()
                
                req = urllib2.Request(url, headers=creatHead())
                html = urllib2.urlopen(req).read()
                html = html.decode('gbk').encode("utf-8")
                    
                if html.find(reLogin) == -1:
                    temp = re.search(reOfferNum, html)
                    if temp:
                        num = int(temp.group(1))
                        print time.strftime("%X "), len(priceList), count, num, price, price - priceStart, priceStart, total 
                    else:
                        print time.strftime("%F %X\t"), "找不到产品数目：", url
                        addPrice = round(addPrice * 2, 2)
                        sleepTime(startTime, random.randint(10, 60))
                        continue
                else:
                    print time.strftime("%F %X\t"), "登陆：", url
                    addPrice = round(addPrice * 2, 2)
                    sleepTime(startTime, random.randint(30, 180))
                    continue
                
            priceList.append(round(price, 2))
            numList.append(num)
            sleepTime(startTime, SLEEP_TIME)
    except Exception, e:
        print 'splitPrice()在', time.strftime("%F %X 发生错误:"), e, url
        return
        
    allNum = numList[0]
    for i in numList[1:]:
        allNum = allNum + i
    print "可抓取的产品数目：%d\t产品的总数目：%d\t遗漏的产品数目：%d" % (allNum, total, total - allNum)
    
    with open("./result/price/" + categoryURL[28:].replace('-', '').replace('.html', '') + "_price.log", 'a') as f:
        f.write(str(len(priceList)) + "\t价格：" + str(priceList) + '\n')
        f.write(str(len(numList)) + "\t数目：" + str(numList) + '\n')
        f.write("可抓取的产品数目：" + str(allNum) + "\t产品的总数目：" + str(total) + "\t遗漏的产品数目：" + str(total - allNum) + '\n\n')
    f.close()
                
    return priceList

def getCompanyURL(categoryURL, priceStart, priceEnd):
    result = []
    beginPage = 0
    idNum = ASYNC_COUNT
    urlTemp = categoryURL + '?beginPage=[beginPage]&uniqfield=userid&asyncCount=' + unicode(ASYNC_COUNT) + '&priceStart=' + unicode(priceStart) + '&priceEnd=' + unicode(priceEnd)
    
    while idNum >= ASYNC_COUNT and beginPage < 101:
        startTime = time.time()
        beginPage = beginPage + 1
        url = urlTemp.replace('[beginPage]', unicode(beginPage))
        if beginPage == 100:
            url = url.replace("asyncCount=" + unicode(ASYNC_COUNT), "asyncCount=200")     
        try:
            req = urllib2.Request(url, headers=creatHead())
            html = urllib2.urlopen(req).read() 
            temp = re.findall(reCompany, html)
            if temp:
                print time.strftime("%X  "), beginPage, len(temp), url
                idNum = len(temp)
                for item in temp:
                    result.append(item)
                sleepTime(startTime, SLEEP_TIME)
            else:
                print time.strftime("%F %X\t"),
                htmlNew = html.decode("gbk").encode("utf8")
                if htmlNew.find("1688/淘宝会员登录") != -1:
                    print "登陆...", url
                    sleepTime(startTime, random.randint(30, 180))
                    beginPage = beginPage - 1
                else:
                    print "没有匹配到结果！", url
                    break
                       
        except Exception, e:
            print 'getCompanyURL()在', time.strftime("%F %X 发生错误:"), e, url
            break
        
    return result


if __name__ == '__main__':
    print os.path.basename(__file__) + '\t程序开始运行：', time.strftime("%Y-%m-%d %X")
    if not os.path.exists('./result'):
        os.mkdir('./result')
    if not os.path.exists('./result/price'):
        os.mkdir('./result/price')
    beginTime = time.time()
   
    categorys = readCategoryFile("./data/category.dat")
    categorysHave = readCategoryFile("./data/category_have.log")
    print  len(categorys),
    for key in categorysHave:
        if categorys.has_key(key):
            del categorys[key]
    print len(categorysHave), len(categorys)  
         
# 将产品根据价格划分可被抓取的范围：
    for categoryURL in categorys:
        print time.strftime("%Y-%m-%d %X\t"), "开始第一步：" 
        step1 = time.time() 
        priceList = splitPrice(categoryURL)
        print "第一步用时：", time.time() - step1
        print time.strftime("%Y-%m-%d %X\t"), "第一步结束。"  
        
# 获取产品的offerId：
        print time.strftime("%Y-%m-%d %X\t"), "开始第二步：" 
        step2 = time.time()   
        i = 0
        tempResult = []
        while i < len(priceList) - 1:
            print "次数:", i, priceList[i], priceList[i + 1]
            tempResult = tempResult + getCompanyURL(categoryURL, priceList[i] + 0.001, priceList[i + 1] + 0.001)
            i = i + 1
        if len(tempResult) > 0:
            result = {}
            for item in tempResult:
                temp = item[1].decode('gbk').encode('utf8')
                if item[1] == '':
                    temp = u'0'
                value = temp + ',' + item[3].decode('gbk').encode('utf8') + ',' + item[4].decode('gbk').encode('utf8')
                result[item[2]] = value
            with open("./result/" + categoryURL[28:].replace('-', '').replace('.html', '') + "_company.csv", "a")as fw:
                for item in result:
                    fw.write(item + u',' + result[item] + u'\n')
            fw.close()
            print len(result)
            with open("./data/category_have.log", 'a') as fwHave:
                fwHave.write(unicode(categoryURL) + u'\t' + unicode(categorys[categoryURL] + u'\n'))
                   
        print "第二步用时：", time.time() - step2
        print time.strftime("%Y-%m-%d %X\t"), "第二步结束。" 
    
    endTime = time.time()
    print '程序运行结束：', time.strftime("%Y-%m-%d %X")
    print "用时：", endTime - beginTime
    pass
