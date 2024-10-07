import joblib
import datetime as DT
import GetModel
import ProcessData
import GetData
from pyecharts.charts import Bar, Grid, Tab, Map, Line
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from pyecharts import options as opts
import pandas as pd
from pyecharts.globals import ThemeType
import webbrowser
import os
tab = Tab()

#今天天气-------------------------
today_data = GetData.getToday(54161)
headers_ = ["日期", "最高温", "最低温", "天气", "风力风向", "空气质量指数"]
rows_ = [
    [today_data['日期'].values[0], today_data['最高温'].values[0],
     today_data['最低温'].values[0], today_data['天气'].values[0],
     today_data['风力风向'].values[0], today_data['空气质量指数'].values[0]]]
def table_main() -> Table:
    return (Table()
            .add(headers_, rows_)
            .set_global_opts(title_opts=ComponentTitleOpts(title="", subtitle="")))
tab = Tab()
tab.add(table_main(), "今日长春")
tab.render("天气网.html")


#未来天气----------------
# 训练并保存模型并返回MAE
r = GetModel.getModel()
print("MAE:", r[0])
# 读取保存的模型
model = joblib.load('Model.pkl')
# 最终预测结果
preds = model.predict(r[1])
preds = model.predict(r[1])
for a in range(7):
    today = DT.datetime.now()
    time = (today + DT.timedelta(days=a)).date()
    print(f"{time.year}-{time.month}-{time.day} "
          f"最高气温 {preds[a][0]}, "
          f"最低气温 {preds[a][1]}, "
          f"空气质量 {preds[a][2]}")
predict_airs = []
predict_low_temperature = []
predict_high_temperature = []
x_data = []
def create_grid_week(x_data, low_temperature, high_temperature, airs) -> Grid:
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("最高温", high_temperature, yaxis_index=0, color="#d14a61")
        .add_yaxis("最低温", low_temperature, yaxis_index=1, color="#5793f3")
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="最高温", type_="value", min_=-30, max_=40, position="right",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#d14a61")),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value", name="天气质量指数", min_=0, max_=300, position="left",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#675bba")),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="最低温", min_=-30, max_=40, position="right", offset=80,
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#5793f3")),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            ),
            title_opts=opts.TitleOpts(title=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "天气质量指数 优(0~50) 良(51~100) 轻度(101~150) 中度(151~200) 重度(201~300)",
            airs, yaxis_index=2, color="#675bba", label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)

for i in range(7):
    predict_high_temperature.append(round(preds[i][0], 4))
    predict_low_temperature.append(round(preds[i][1], 4))
    predict_airs.append(round(preds[i][2], 4))
    x_data.append((today + DT.timedelta(days=i)).date())
def grid_week_predict() -> Grid:
    return create_grid_week(x_data, predict_low_temperature, predict_high_temperature, predict_airs)
tab.add(grid_week_predict(), "未来长春")
tab.render("天气网.html")

#最近一周的天气
week_data = GetData.getWeek(54161)
airs = ProcessData.setAir(week_data)
low_temperature = ProcessData.setLowTemp(week_data)
high_temperature = ProcessData.setHighTemp(week_data)
def create_grid_week(x_data, low_temperature, high_temperature, airs) -> Grid:
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("最高温", high_temperature, yaxis_index=0, color="#d14a61")
        .add_yaxis("最低温", low_temperature, yaxis_index=1, color="#5793f3")
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="最高温", type_="value", min_=-30, max_=40, position="right",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#d14a61")),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value", name="天气质量指数", min_=0, max_=300, position="left",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#675bba")),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="最低温", min_=-30, max_=40, position="right", offset=80,
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#5793f3")),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            ),
            title_opts=opts.TitleOpts(title=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "天气质量指数 优(0~50) 良(51~100) 轻度(101~150) 中度(151~200) 重度(201~300)",
            airs, yaxis_index=2, color="#675bba", label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)

tab.add(create_grid_week(["前七天", "前六天", "前五天", "前四天", "前三天", "前两天", "前一天"], low_temperature,
                             high_temperature, airs), "近一周长春")
tab.render("天气网.html")

#今日中国天气
provinces = [
    "黑龙江", "内蒙古", "吉林", "辽宁", "河北", "天津", "山西", "陕西",
    "甘肃", "宁夏", "青海", "新疆", "西藏", "四川", "重庆", "山东", "河南",
    "江苏", "安徽", "湖北", "浙江", "福建", "江西", "湖南", "贵州",
    "广西", "海南", "上海", "广东", "云南"
]
def setData(column, i):
    return china_today.iloc[i][column]
china_today = GetData.getChinaToday()
china_today = china_today.fillna({"最低温": 0, "最高温": 0, "天气": "未知", "风力风向": "未知", "空气质量指数": 0})
rows = []
for i in range(len(provinces)):
    rows.append([provinces[i], setData('最低温', i), setData('最高温', i), setData('天气', i), setData('风力风向', i)])
def today_china_table() -> Table:
    return (Table()
            .add(["省份", "最低温", "最高温", "天气", "风力风向"], rows)
            .set_global_opts(
                title_opts=ComponentTitleOpts(title="今日全国各省会城市的天气信息表", subtitle="")
            ))
tab.add(today_china_table(), "今日中国天气")
tab.render("天气网.html")

#全国空气状况
provinces = [
    "黑龙江省", "内蒙古自治区", "吉林省", "辽宁省", "河北省", "天津市", "山西省", "陕西省",
    "甘肃省", "宁夏回族自治区", "青海省", "新疆维吾尔自治区", "西藏自治区", "四川省", "重庆市", "山东省", "河南省",
    "江苏省", "安徽省", "湖北省", "浙江省", "福建省", "江西省", "湖南省", "贵州省",
    "广西壮族自治区", "海南省", "上海市", "广东省", "云南省"
]
china_today = GetData.getChinaToday()
china_today = china_today.fillna({"最低温": 0, "最高温": 0, "天气": "未知", "风力风向": "未知", "空气质量指数": 0})
china_airs = ProcessData.setAir(china_today)
print(china_airs)
airs_list = [china_airs[i] for i in range(len(provinces))]
print(airs_list)
print(len(airs_list))
print(len(provinces))
def today_china() -> Map:
    c = (
        Map(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add("空气质量指数", [list(z) for z in zip(provinces, airs_list)], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="今日中国空气质量"),
            visualmap_opts=opts.VisualMapOpts(
                max_=300,
                min_=0,
                is_piecewise=True,
                pieces=[
                    {"min": 0, "max": 50, "label": "优 (0~50)", "color": "#00FF00"},
                    {"min": 51, "max": 100, "label": "良 (51~100)", "color": "#FFFF00"},
                    {"min": 101, "max": 150, "label": "轻度污染 (101~150)", "color": "#FF7E00"},
                    {"min": 151, "max": 200, "label": "中度污染 (151~200)", "color": "#FF0000"},
                    {"min": 201, "max": 300, "label": "重度污染 (201~300)", "color": "#990000"},
                ],
            ),
            tooltip_opts=opts.TooltipOpts(
                formatter="{b}: {c}"  # {b} 表示省份名称，{c} 表示空气质量指数
            ),
        )
    )
    return c
# 渲染地图
map_chart = today_china()
output_file = "天气网.html"
map_chart.render(output_file)

# 自动打开生成的 HTML 文件
webbrowser.open('file://' + os.path.realpath(output_file))
'''
# 训练并保存模型并返回MAE
r = GetModel.getModel()
print("MAE:", r[0])

# 读取保存的模型
model = joblib.load('Model.pkl')

# 最终预测结果
preds = model.predict(r[1])

print("未来7天预测")
for a in range(7):
    today = DT.datetime.now()
    time = (today + DT.timedelta(days=a)).date()
    # print(f"{time.year}-{time.month}-{time.day} "
    #       f"最高气温 {preds[a][0]}, "
    #       f"最低气温 {preds[a][1]}, "
    #       f"空气质量 {preds[a][2]}")
print('ok')
# 获取当日长春天气数据
today_data = GetData.getToday(54161)
headers_ = ["日期", "最高温", "最低温", "天气", "风力风向", "空气质量指数"]
rows_ = [
    [today_data['日期'].values[0], today_data['最高温'].values[0],
     today_data['最低温'].values[0], today_data['天气'].values[0],
     today_data['风力风向'].values[0], today_data['空气质量指数'].values[0]],
]

def table_main() -> Table:
    return (Table()
            .add(headers_, rows_)
            .set_global_opts(title_opts=ComponentTitleOpts(title="", subtitle="")))
# 获取最近七天的天气数据
week_data = GetData.getWeek(54161)
airs = ProcessData.setAir(week_data)
low_temperature = ProcessData.setLowTemp(week_data)
high_temperature = ProcessData.setHighTemp(week_data)

def create_grid_week(x_data, low_temperature, high_temperature, airs) -> Grid:
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("最高温", high_temperature, yaxis_index=0, color="#d14a61")
        .add_yaxis("最低温", low_temperature, yaxis_index=1, color="#5793f3")
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="最高温", type_="value", min_=-30, max_=40, position="right",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#d14a61")),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value", name="天气质量指数", min_=0, max_=300, position="left",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#675bba")),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)),
            )
        )
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="最低温", min_=-30, max_=40, position="right", offset=80,
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#5793f3")),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
            ),
            title_opts=opts.TitleOpts(title=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "天气质量指数 优(0~50) 良(51~100) 轻度(101~150) 中度(151~200) 重度(201~300)",
            airs, yaxis_index=2, color="#675bba", label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)


# 获取当日长春天气数据
today_data = GetData.getToday(54161)
today_data = today_data.fillna({"日期": "未知", "最高温": 0, "最低温": 0, "天气": "未知", "风力风向": "未知", "空气质量指数": 0})

# 读取最近七天的天气数据
week_data = GetData.getWeek(54161)
week_data = week_data.fillna({"天气": "未知", "最低温": 0, "最高温": 0})

# 获取全国各省会城市今日的天气情况
china_today = GetData.getChinaToday()
china_today = china_today.fillna({"最低温": 0, "最高温": 0, "天气": "未知", "风力风向": "未知", "空气质量指数": 0})

# 确保在 setAir 函数中处理缺失值
def setAir(data):
    airs = []
    for i in data['空气质量']:
        if isinstance(i, str):  # 确保是字符串
            i = i.split(' ')[0]
            airs.append(i)
        elif pd.isna(i):  # 检查是否为缺失值
            airs.append(0)  # 使用默认值
    return airs

# 预测长春一周的天气和空气
predict_airs = []
predict_low_temperature = []
predict_high_temperature = []
x_data = []

for i in range(7):
    predict_high_temperature.append(round(preds[i][0], 4))
    predict_low_temperature.append(round(preds[i][1], 4))
    predict_airs.append(round(preds[i][2], 4))
    x_data.append((today + DT.timedelta(days=i)).date())

def grid_week_predict() -> Grid:
    return create_grid_week(x_data, predict_low_temperature, predict_high_temperature, predict_airs)
# 获取全国各省会城市今日的天气情况
china_today = GetData.getChinaToday()
china_today.to_csv("china_today.csv", index=False)



provinces = [
    "黑龙江", "内蒙古", "吉林", "辽宁", "河北", "天津", "山西", "陕西",
    "甘肃", "宁夏", "青海", "新疆", "西藏", "四川", "重庆", "山东", "河南",
    "江苏", "安徽", "湖北", "浙江", "福建", "江西", "湖南", "贵州",
    "广西", "海南", "上海", "广东", "云南", "台湾"
]

rows = []
for i in range(len(provinces)):
    rows.append([provinces[i], setData('最低温', i), setData('最高温', i), setData('天气', i), setData('风力风向', i)])

def today_china_table() -> Table:
    return (Table()
    .add(["省份", "最低温", "最高温", "天气", "风力风向"], rows)
    .set_global_opts(
        title_opts=ComponentTitleOpts(title="今日全国各省会城市的天气信息表", subtitle="")
    ))

china_airs = ProcessData.setAir(china_today)
airs_list = [china_airs[i] for i in range(len(provinces))]

def today_china() -> Map:
    return (Map()
    .add("天气质量指数 优(0~50) 良(51~100) 轻度(101~150) 中度(151~200) 重度(201~300)",
         [list(z) for z in zip(provinces, airs_list)], "china")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="今日中国空气质量"),
        visualmap_opts=opts.VisualMapOpts(max_=300),
    ))

# 分页图的标题

tab.add(table_main(), "今日长春")
tab.add(grid_week_predict(), "未来长春")
tab.add(create_grid_week(["前七天", "前六天", "前五天", "前四天", "前三天", "前两天", "前一天"], low_temperature, high_temperature, airs), "近一周长春")
tab.add(today_china_table(), "今日中国天气")
tab.add(today_china(), "今日全国空气质量")

'''