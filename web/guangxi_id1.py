import requests
from bs4 import BeautifulSoup
import time
import re
import random
import logging
import socket
import base64
from postgresql import driver
import postgresql
import json

logging.basicConfig(level=logging.DEBUG)

'广西ID抓取'

DB = driver.connect(host='', user='gxj', password='', database='', port=)


# 数据库异常重新连接
def conn_sql():
    global DB
    if DB.closed:
        DB = postgresql.driver.connect(host='106.75.145.80', user='gxj', password='xiaojun.guo1', database='cra1', port=9988)
    return DB


# 产生随机数
def rangenum():
    little = random.randint(1, 1900000)
    more = little+1000
    return little, more


# 插入数据库
def insert_sql(key_word, sql_body):
    sql_body = json.dumps(sql_body, ensure_ascii=False)
    sql_insert = """insert into org_guangxi_id_new ("id", "body", "flag") values('{}', '{}', '0')""".format(key_word, sql_body)
    DB.query(sql_insert)
    logging.warning('   插入数据库成功  time  = {}   '.format(time.ctime()))


# 从数据库中获得id
def get_id(m, n):
    sql_sur = """select "regNo" from gx_id_new where id > '{}' and id < '{}' and flag='0' limit 100;""".format(m, n)
    result = DB.query(sql_sur)
    result_id = [i[0] for i in result]
    return result_id


# 更新数据库中的used字段
def update(used_id):
    sql_update = """update gx_id_new set flag = '1' where "regNo" = '{}';""".format(used_id)
    DB.query(sql_update)


# 获得32位随机字符串
def random_list():
    a = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
         'h', 'i', 'j', 'k', 'l', 'm', 'n', 'u', 'q', 'p', 'w', 'y', 'z', 'r', 's', 't',
         '0', 'w', 'o']
    m = [random.randint(0, 32) for _ in range(32)]
    l = ''
    for i in m:
        l = l + a[i]
    return l


# 对数据页面进行解析
# def analysis(soupstr):
#     company_name = soupstr.select('h3.title')[0].select('span')[0].get_text().replace(' ', '').replace('\n', '').replace('	', '').replace('\r', '')
#     onclick = soupstr.select('table.t-info')[0].get('onclick')
#     href = onclick.split('"')[1]
#     entid = href.split('=')[1].split('&')[0]
#     td = [i.get_text().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '') for i in
#           soupstr.select('table.t-info')[0].select('td')]
#     td_text = [i.split('：')[1] for i in td]
#     return entid, href, td_text, company_name


# 对数据页面进行解析
def analysis(soupstr):
    entid_l, href_l, td_text_l, company_name_l = [], [], [], []
    part_div = soupstr.select('div.search-result')
    # 判断此注册号有内容
    if part_div[0].select('li'):
        part_li = part_div[0].select('li')
        for i in part_li:
            company_name = i.select('h3.title')[0].select('span')[0].get_text().replace(' ', '').replace('\n','').replace('	', '').replace('\r', '')
            onclick = i.select('table.t-info')[0].get('onclick')
            href = onclick.split('"')[1]
            entid = href.split('=')[1].split('&')[0]
            td = [j.get_text().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '') for j in i.select('table.t-info')[0].select('td')]
            td_text = [i.split('：')[1] for i in td]
            entid_l.append(entid)
            href_l.append(href)
            td_text_l.append(td_text)
            company_name_l.append(company_name)
        return entid_l, href_l, td_text_l, company_name_l


# 通过注册号获取id数据
def spider(regno):
    s = requests.session()
    # 请求首页
    url_index = 'http://gx.gsxt.gov.cn/sydq/loginSydqAction!sydq.dhtml'
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    }
    s.get(url_index, timeout=15)

    # 请求时间戳url
    t = str(time.time()).split('.')[0] + str(time.time()).split('.')[-1][:3]
    url1 = 'http://gx.gsxt.gov.cn/pc-geetest/register?t=' + t
    url1_headers = {
        'Host': 'gx.gsxt.gov.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://gx.gsxt.gov.cn/sydq/loginSydqAction!sydq.dhtml',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    rel1 = s.get(url1, headers=url1_headers, timeout=15)
    challenge = eval(rel1.text)['challenge']

    url2 = 'http://gx.gsxt.gov.cn/pc-geetest/validate'
    random32 = random_list()
    randomj = random32 + '|jordan'
    date2 = {
        'geetest_challenge': (challenge + 'kl'),
        'geetest_validate': random_list,
        'geetest_seccode': randomj
    }
    s.post(url2, data=date2, timeout=15)
    url3 = 'http://gx.gsxt.gov.cn/es/esAction!entlist.dhtml?urlflag=0&challenge=' + challenge + 'kl'
    date3 = {
        'nowNum': '',
        'keyword': regno,
        'urlflag': '0',
        'clear': '请输入企业名称、统一社会信用代码或注册号'
    }
    url3_headers = {
        'Cache-Control': 'max-age=0',
        'Origin': 'http://gx.gsxt.gov.cn',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    rel3 = s.post(url3, data=date3, headers=url3_headers, timeout=15)
    # print(rel3.text)
    soup = BeautifulSoup(rel3.text, 'lxml')
    url_id, href_id, regno_l, company = analysis(soup)
    for i in url_id:
        # print(i)
        body = {}
        index = url_id.index(i)
        body['href'] = href_id[index]
        body['entid'] = url_id[index]
        body['regNo'] = regno_l[index][0]
        body['companyName'] = company[index]
        body['creationData'] = regno_l[index][-1]
        body['legalrepresentative'] = regno_l[index][1]
        print(json.dumps(body, ensure_ascii=False))
        try:
            insert_sql(i, body)
            # print(regno_l[index][0])
            update(regno_l[index][0])
        except Exception:
            logging.warning('重复数据')
            continue


def main():

    upper, lower = rangenum()
    reg_id = get_id(upper, lower)
    # reg_id = ['00000']
    if len(reg_id) == 0:
        return '爬取完毕'
    else:
        for i in reg_id:
            t = random.randint(0, 4)
            try:
                time.sleep(t)
                spider(i)

            except Exception:
                continue


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            logging.warning('  main函数except   = {}'.format(e))
            DB.close()
            # 重新连接数据库
            conn_sql()
            time.sleep(10)
            continue
    DB.closed()

