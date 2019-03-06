from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery
import time
import datetime
import mysqltool

#插入字符串拼接
def get_insert_sql(table,list):
    values=','.join(['%s']*len(list[0]))
    return 'INSERT INTO {table}(city,region,rown,name,house_type,house_information,house_area,house_time,house_cost,house_univalence,house_people) ' \
           'VALUES ({values})'.format(table=table,values=values)

#日期格式化
def get_date(newtime):
    if newtime=='1天前':
        day=datetime.timedelta(days=1)
        newtime=(datetime.datetime.now()-day).strftime('%Y/%m/%d')
    elif newtime=='2天前':
        day = datetime.timedelta(days=2)
        newtime = (datetime.datetime.now() - day).strftime('%Y/%m/%d')
    elif newtime=='3天前':
        day = datetime.timedelta(days=3)
        newtime = (datetime.datetime.now() - day).strftime('%Y/%m/%d')
    return newtime

#获取地区
def get_region(html):
    doc=PyQuery(html,parser="html")
    items=doc('.section-condition .section .base-termcont .filter-block .termcon a').items()
    for item in items:
        url='https://tj.centanet.com'+item.attr('href')
        browser.get(url)
        get_town(browser.page_source,item.text())

#获取乡镇
def get_town(html,region):
    doc = PyQuery(html, parser="html")
    items = doc('.section-condition .section .base-termcont .filter-block .subterm a').items()
    for item in items:
        url = 'https://tj.centanet.com' + item.attr('href')
        browser.get(url)
        index_page(browser.page_source,region,url,item.text())

#获取数据
def index_page(html,region,parturl,town):
    doc=PyQuery(html,parser='html')
    try:
        while True:
            items = doc('.section-transaRecord .section .tablerecord-list .tablerecond-item a').items()
            list = []
            for item in items:
                list1 = ['天津',region,town,item.find('.w_1').text()]
                for ite in item.find('.w_3').items():
                    list1.append(ite.text())
                list.append(list1)

            newList = []
            for partLits in list:
                data = {
                    '城市':partLits[0],
                    '地区':partLits[1],
                    '乡镇':partLits[2],
                    '楼盘':partLits[3],
                    '户型':partLits[4],
                    '房源情况':partLits[5],
                    '面积':float(partLits[6][:-1]),
                    '成交时间':get_date(partLits[7]),
                    '成交价':float(partLits[8][:-1]),
                    '单价':float(partLits[9][:-3]),
                    '经纪人':partLits[10]
                }
                newList.append(tuple(data.values()))
            db.Insert(get_insert_sql('tjhpi', newList), newList)  # 批量插入  tuple()方法list转元组

            input = browser.find_element(By.CSS_SELECTOR, '.section-pager .section .pager-box .pager-inner')
            btn = input.find_element(By.XPATH, "./a[contains(text(),'>')]")  # 使用xpath选择器定位到a标签下文本为>的地方

            btn.click()
            time.sleep(3)
            doc=PyQuery(browser.find_element_by_xpath('//*').get_attribute('outerHTML'),parser='html')
    except Exception as e:
        print(town+'爬取完成')
        time.sleep(5)

db=mysqltool.MySQLTool(host='localhost',user='root',pwd='root',db='python')
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 2)
browser.get('https://tj.centanet.com/chengjiao/')
get_region(browser.page_source)


# sql='create table tjhpi(' \
#     'id int PRIMARY KEY,' \
#     'name VARCHAR(20),' \
#     'region VARCHAR(20),' \
#     'house_type VARCHAR(20),' \
#     'house_information VARCHAR(20),' \
#     'house_area DOUBLE,' \
#     'house_time VARCHAR(20),' \
#     'house_cost DOUBLE,' \
#     'house_univalence DOUBLE,' \
#     'house_people VARCHAR(20)' \
#     ')'
# db.Insert(sql)



