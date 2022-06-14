
from gevent import pywsgi
from flask.json import jsonify
from flask import Flask, render_template
import utils
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode

app = Flask(__name__, static_folder="templates")
x_data = utils.getx()
y_data = utils.gety()
#last_day = getData.singleDay()
for i in range(13):
    y_data[i][:] = [x - y_data[i][-1] for x in y_data[i]]

background_color_js = (
    "{new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#b75d83'}, {offset: 1, color: '#06a7ff'}], false)}"
)
area_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
)

area_color_js1 = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#e06666'}, {offset: 1, color: '#3fbbff0d'}], false)")

area_color_js2 = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#e02266'}, {offset: 1, color: '#3fbbff0d'}], false)")


def line_base() -> Line:
    line = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
        .add_xaxis(x_data)
        .add_yaxis(
            series_name="外国语学院",
            y_axis=y_data[11],
            is_smooth=True,
            stack="总量",
            is_symbol_show=True,
            symbol="circle",
            symbol_size=3,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(
                is_show=False, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger='axis'),
            areastyle_opts=opts.AreaStyleOpts(
                color=JsCode(area_color_js), opacity=1),
        )
        .add_yaxis(
            series_name="大数据与互联网学院",
            y_axis=y_data[1],
            is_smooth=True,
            is_symbol_show=True,
            stack="总量",
            symbol="circle",
            symbol_size=3,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(
                is_show=False, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="#66f", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis"),
            areastyle_opts=opts.AreaStyleOpts(
                color=JsCode(area_color_js1), opacity=0.8),
        )
        .add_yaxis(
            series_name="城市交通与物流学院",
            y_axis=y_data[3],
            is_smooth=True,
            is_symbol_show=True,
            stack="总量",
            symbol="circle",
            symbol_size=3,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(
                is_show=False, position="top", color="#fff"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="#281", border_color="#fff", border_width=3
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True, trigger="axis"),
            areastyle_opts=opts.AreaStyleOpts(
                color=JsCode(area_color_js2), opacity=0.8),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="2022-SZTU网站评比投票活动",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(
                    color="#fff", font_size=15),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(
                type_="time",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=True),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                is_scale=False,
                # min_=3000,
                # max_=3000,
                position="right",
                split_number=10,
                offset=0,
                axislabel_opts=opts.LabelOpts(
                    is_show=False, margin=5, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        width=2, color="#fff")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=False,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            legend_opts=opts.LegendOpts(is_show=True),
            # toolbox_opts=opts.TooltipOpts(is_show=True)
        )
    )
    return line


@ app.route("/")
def index():
    return render_template("index.html")


@ app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


@ app.route("/lineDynamicData")
def update_line_data():
    res = getData.getDynamic()
    return jsonify({"time": res[0], "value": res[1]})


if __name__ == "__main__":
    #app.debug = True
    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
    server.serve_forever()
