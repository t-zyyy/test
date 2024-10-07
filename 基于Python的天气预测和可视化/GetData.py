import pandas as pd
import requests
import datetime
import time
import random

from io import StringIO  # 添加这一行
import html5lib
import lxml
# 提供年份和月份，爬取对应的表格数据
url = "http://tianqi.2345.com/Pc/GetHistory"
headers = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "http://tianqi.2345.com"
}

def craw_table(id, year, month):
    params = {
        "areaInfo[areaId]": id,
        "areaInfo[areaType]": 2,
        "date[year]": year,
        "date[month]": month
    }
    try:
        resq = requests.get(url, headers=headers, params=params)
        resq.raise_for_status()  # 检查请求是否成功
        #print(resq)
        data = resq.json().get("data")
       # print(data)
        if not data:
            print(f"警告: 第{year}年{month}月，未获取到有效数据！")
            return pd.DataFrame()  # 返回空的 DataFrame

        # 使用 StringIO 来处理 HTML 数据
        df = pd.read_html(StringIO(data))[0]
        return df
    except requests.HTTPError as e:
        print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
        return pd.DataFrame()  # 返回空的 DataFrame
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return pd.DataFrame()  # 返回空的 DataFrame
    except ValueError as e:
        print(f"JSON解析错误: {e}")
        return pd.DataFrame()  # 返回空的 DataFrame

# 输入城市id，爬取该城市今日的天气数据
def getToday(id):
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    month_data = craw_table(id, year, month)
    time.sleep(random.uniform(0.2, 0.5))  # 随机延时 1 到 3 秒
    if month_data.empty:
        return month_data  # 如果没有数据，返回空 DataFrame
    return month_data.tail(1)

# 输入城市id，爬取该城市近七天的天气数据
def getWeek(id):
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    month_data = craw_table(id, year, month)
    time.sleep(random.uniform(0.2, 0.5))  # 随机延时 1 到 3 秒
    if month_data.empty:
        return month_data  # 如果没有数据，返回空 DataFrame
    return month_data.tail(7)

# 爬取全国各个省会城市的今日的天气数据
def getChinaToday():
    ids = [
        50953, 53463, 54161, 54342, 53698, 54527, 53772, 57036,
        52889, 53614, 52866, 51463, 55591, 56294, 57516, 54823,
        57083, 58238, 58321, 57494, 58457, 58847, 58606, 57687,
        57816, 59431, 59758, 58362, 59287, 56778
    ]
    list_data = []
    for i in ids:
        df = getToday(i)
        if not df.empty:
            list_data.append(df)
        else:
            print(f"未获取到城市 ID {i} 的今日天气数据。")
        time.sleep(random.uniform(0.2, 0.5))  # 随机延时 1 到 3 秒
    return pd.concat(list_data).reset_index(drop=True) if list_data else pd.DataFrame()

# 获取长春最近3年的天气数据，用于预测
def getYears():
    today = datetime.datetime.today()
    df_list = []
    for year in range(today.year - 3, today.year + 1):  # 修改为3年
        for month in range(1, 13):
            df = craw_table(54161, year, month)
            if not df.empty:
                df_list.append(df)
            else:
                print(f"未获取到长春{year}年{month}月的天气数据。")
            time.sleep(random.uniform(0.2, 0.5))  # 随机延时 1 到 3 秒
    return pd.concat(df_list).reset_index(drop=True) if df_list else pd.DataFrame()

# 传入一个时间范围，获取某个时间范围的天气数据
def getPredictDate(year0, month0, day0, year1, month1, day1):
    id = 54161
    date_list = []
    if month0 != month1:
        date0 = craw_table(id, year0, month0)
        date_ago = date0[day0 - 1:] if not date0.empty else pd.DataFrame()
        time.sleep(random.uniform(0.2, 0.5))  # 随机延时 1 到 3 秒
        date1 = craw_table(id, year1, month1)
        date_pre = date1[:day1] if not date1.empty else pd.DataFrame()

        if not date_ago.empty:
            date_list.append(date_ago)
        if not date_pre.empty:
            date_list.append(date_pre)

        date = pd.concat(date_list).reset_index(drop=True) if date_list else pd.DataFrame()
    else:
        date0 = craw_table(id, year0, month0)
        date = date0[day0 - 1:day1] if not date0.empty else pd.DataFrame()
    return date




# 示例用法
if __name__ == '__main__':
    # 获取长春今日的天气数据
    today_data = getToday(54161)
    print("ok")
    # print("长春今日天气数据:")
    # print(today_data)
    #
    # # 获取全国各省会城市的今日天气数据
    # china_today_data = getChinaToday()
    # print("全国各省会城市今日天气数据:")
    # print(china_today_data)
    #
    # # 获取长春最近3年的天气数据
    # years_data = getYears()
    # print("长春最近3年的天气数据:")
    # print(years_data)
