import requests
from requests.cookies import RequestsCookieJar
import json


def get_score(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total = requests.get("https://pc-api.xuexi.cn/open/api/score/get", cookies=jar).content.decode("utf8")
        total = int(json.loads(total, encoding="utf8")["data"]["score"])
        myscores = {'总积分': total}
        each = requests.get("https://pc-api.xuexi.cn/open/api/score/today/queryrate", cookies=jar).content.decode(
            "utf8")
        # 用户ID
        others = json.loads(each, encoding="utf8")["data"]
        myscores.update({i: others[i] for i in ['userId', 'inBlackList', 'blackListTip']})

        # each = json.loads(each, encoding="utf8")["data"]["dayScoreDtos"]
        each = others['dayScoreDtos']
        todayscore = 0
        for i in each:
            todayscore += int(i["currentScore"])
        myscores.update({'今日积分': todayscore})

        myscores.update({i['name']: int(i["currentScore"]) for i in each})  # if i["ruleId"] in [1, 2, 9, 1002, 1003]})
        myscores.update({i['name']+'目标': int(i["dayMaxScore"]) for i in each})
        # each = [int(i["currentScore"]) for i in each if i["ruleId"] in [1, 2, 9, 1002, 1003]]
        # print(myscores)
        return myscores
    except:
        print("=" * 120)
        print("get_score获取失败")
        print("=" * 120)
        raise
def get_diandian(cookies):
    try:
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        total = requests.get("https://pc-proxy-api.xuexi.cn/api/point/get", cookies=jar).content.decode("utf8")
        total = int(json.loads(total, encoding="utf8")["data"]["pointString"])
        mydian = {'点点通': total}
        each = requests.get("https://pc-proxy-api.xuexi.cn/api/point/today/queryrate", cookies=jar).content.decode(
            "utf8")

        todaydian = int(json.loads(each, encoding='utf8')['data']['dayEarnPoint'])
        mydian.update({'今日点点通': todaydian})

        others = json.loads(each, encoding="utf8")["data"]["taskProgressDtos"]
        # each = [int(i['completedCount']) for i in each]
        # j = 6 # 每几题算一级
        mydian.update({i['taskName']: int(i['completedCount']) * int(i['target'])+int(i['progress']) % int(i['target'])
                       for i in others})
        mydian.update({i['taskName']+'目标': int(i['maxCompletedCount']) * int(i['target']) for i in others})
        # each = [int(i[j]) for j in ['completedCount','progress'] for i in each] # if i["ruleId"] in [1, 2, 9, 1002, 1003]]
        # print('diandian',each)
        # print(mydian)
        return mydian
    except:
        print("=" * 120)
        print("get_diandian获取失败")
        print("=" * 120)
        raise