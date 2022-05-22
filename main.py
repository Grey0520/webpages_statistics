import time
import utils

second = utils.sleep_time(0, 0, 2)


def sql():
    while True:

        dic = utils.getData()
        if dic["code"] == 200:
            utils.saveData(dic)
        else:
            print(time.now(), "出问题了,100s后重新尝试")
            time.sleep(100 * second)
        # 休眠时间，单位：秒
        time.sleep(10 * second)


if __name__ == '__main__':
  sql()