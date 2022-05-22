import pymongo
from datetime import datetime
import requests


def getHeaders():
    '''
    这个函数的存在，是为了当getData请求失败的时候可以方便修改cookie
    返回一个字典类型的请求头
    '''

    cookie = 'login=1; userInfo=%7B%22username%22%3A%22oGRH1vlxuLpWeqzdbPHDNVj8QZe0%22%2C%22nickname%22%3Anull%2C%22avatar_url%22%3A%22https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2F3ibriatn6eRUeiavjK5XgWHtiaB1Bu6syBaTgNYvVOdep0QibBmEVEh6TbMwpqqpib47icLlmt1yXgTppaAfXeDbnYCkA%2F132%22%2C%22gender%22%3A0%2C%22gender_display%22%3A%22%E7%94%B7%22%2C%22is_init%22%3Atrue%7D; _uab_collina=165288839503717240707897'
    auth = 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NTk0LCJ1c2VybmFtZSI6Im9HUkgxdmx4dUxwV2VxemRiUEhETlZqOFFaZTAiLCJleHAiOjE2NTMzODY1OTIsImVtYWlsIjoiIn0.hCil7vX31VhX5NZN3XdslaqJeAs-KYL6Kzg3Qktw9ok'

    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.3.1(0x13030110) Safari/605.1.15 NetType/WIFI',
        'authorization': auth,
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
    myclient = pymongo.MongoClient(
        "mongodb://user60972586:Sztu0520@dds-wz9jmh3t1y3u133m-pub.mongodb.rds.aliyuncs.com:3717/admin")
    mydb = myclient["webpage_statistic"]

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
