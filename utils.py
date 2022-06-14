import pymongo
from datetime import datetime
import requests
from flask.json import jsonify
from flask import Flask, render_template
from xmlrpc.client import DateTime
import pymongo
from datetime import datetime, timezone, timedelta
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode

beijing = timezone(timedelta(hours=8))
myclient = pymongo.MongoClient(
    "mongodb://user60972586:Sztu0520@dds-wz9jmh3t1y3u133m-pub.mongodb.rds.aliyuncs.com:3717/admin")
mydb = myclient["webpage_statistic"]

# print(mydb.list_collection_names())
mycol = mydb["data1"]
x = mycol.find().sort("time", -1).limit(6000)

xx = []
y = []
for i in range(14):
    y.append([])


def sortSecond(val):
    return val[1]


x.sort("_id", -1)
for i in x:
    # a = datetime.strptime(i['time'],'%H时%M分%S秒')
    # .replace(tzinfo=utc)
    utc = timezone.utc
    t = i['time']
    if(t.second < 6 and t.minute % 40 == 0):

        # m_s = str(t.hour) + ":" + str(t.minute).zfill(2) + \
        #    ":" + str(t.second).zfill(2)
        # .astimezone(beijing)
        xx.append(t)
        # print(t.astimezone(beijing))

        yy = []
        for j in i['content']['data']['list']:
            tup = (j['num'], j['id'])
            yy.append(tup)
        yy.sort(key=sortSecond)
        for j in range(13):
            y[j].append(yy[j][0])

        # yy1.append(i['content']['data']['list'][0]['num'])
        # yy2.append(i['content']['data']['list'][1]['num'])

# y = [yy1, yy2]


def getx():

    return xx


def gety():
    return y


def getDynamic():
    res = []
    d = mycol.find().sort("_id", -1).limit(1)
    t = d[0]['time']
    print(t)
    if t.second <= 10:
        res.append(t)
        yy = []
        d_y = []
        for i in range(14):
            d_y.append([])
        for j in d[0]['content']['data']['list']:
            tup = (j['num'], j['id'])
            yy.append(tup)
        yy.sort(key=sortSecond)
        for j in range(13):
            d_y[j].append(yy[j][0])

        res.append(d_y)
    return res


def singleDay():
    init_data = mycol.find_one({'time': '2022-05-25T15:59:59.615+00:00'})
    res = []

    for j in init_data['content']['data']['list']:
        tup = (j['num'], j['id'])
        res.append(tup)
    res.sort(key=sortSecond)

    return res


# myclient = pymongo.MongoClient(
#     "mongodb://user60972586:Sztu0520@dds-wz9jmh3t1y3u133m-pub.mongodb.rds.aliyuncs.com:3717/admin")
# mydb = myclient["webpage_statistic"]


def getHeaders():
    '''
    这个函数的存在，是为了当getData请求失败的时候可以方便修改cookie
    返回一个字典类型的请求头
    '''

    cookie = 'login=1; userInfo=%7B%22username%22%3A%22oGRH1vtSLHhA2h45ERQP56na4BWI%22%2C%22nickname%22%3Anull%2C%22avatar_url%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FeeNOjYeB0PyicPEGI51ibqXBwAy83AsrEdYIQicfCc1Ul5srKwPN0BW55tsbibfgE9WVJw6IzBPVNScIMW7n9SK3LA%2F132%22%2C%22gender%22%3A0%2C%22gender_display%22%3A%22%E7%94%B7%22%2C%22is_init%22%3Atrue%7D; _uab_collina=165319528412493553342014'
    authorization = 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NTU0LCJ1c2VybmFtZSI6Im9HUkgxdnRTTEhoQTJoNDVFUlFQNTZuYTRCV0kiLCJleHAiOjE2NTM2NjY2NTUsImVtYWlsIjoiIn0.tW7-h-qnwri3Lc7eobsb74rmPEl1zLf2H4FgzwHU5kk'

    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.3.1(0x13030110) Safari/605.1.15 NetType/WIFI',
        'authorization': authorization,
        'host': 'vote.sztu.edu.cn',
        'referer': 'https://vote.sztu.edu.cn/rank',

        'accept-encoding': 'gzip, deflate, br',
        'cookie': cookie,
        'accept-language': 'zh-CN,zh-Hans;q=0.9',
        'accept': '*/*',
    }
    return header


def getData():
    """
    用于获取当前这个时间点的学院网站数据。
    返回值是字典数据，可以直接放到MongoDB上
    """
    url = ('https://vote.sztu.edu.cn/api/vote/rank')
    #url1 = ('https://vote.sztu.edu.cn/api/vote/rank')

    parm = {"project_id": 1}
    # 'timestamp':'1652846522' 抓包的时候发现参数里有这个，但实际测试中不加这个也没关系
    headers = getHeaders()
    r = requests.get(url, params=parm, headers=headers)
    j = r.json()
    dic = j
    #dic = json.dumps(j, ensure_ascii=False, indent=2)
    return dic


def saveData(dic):
    '''
    保存数据到MongoDB上
    '''

    mycol = mydb["data2"]
    a = datetime.now()
    mydict = {
        "time": a,
        "content": dic,
    }
    x = mycol.insert_one(mydict)
    print(x.inserted_id)


def sleep_time(time_hour, time_min, time_second):
    '''
    用来设定定时器
    '''
    return time_hour * 3600 + time_min * 60 + time_second


