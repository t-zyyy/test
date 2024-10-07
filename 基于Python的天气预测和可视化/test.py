from pyecharts import options as opts
from pyecharts.charts import Map
import webbrowser
import os

# 官方示例数据
provinces = ["北京", "天津", "上海", "重庆", "河北", "河南", "云南", "辽宁", "黑龙江", "湖南", "安徽", "山东", "新疆", "江苏", "浙江", "江西", "湖北", "广西", "甘肃", "山西", "内蒙古", "陕西", "吉林", "福建", "贵州", "广东", "青海", "西藏", "四川", "宁夏", "海南", "台湾", "香港", "澳门"]
airs_list = [30, 60, 80, 120, 180, 250, 40, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]

def today_china() -> Map:
    c = (
        Map()
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
        )
    )
    return c

# 渲染地图并保存为 HTML 文件
map_chart = today_china()
output_file = "天气网.html"
map_chart.render(output_file)

# 自动打开生成的 HTML 文件
webbrowser.open('file://' + os.path.realpath(output_file))
