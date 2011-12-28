# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1306272587.736769
_template_filename='/home/god/Dropbox/f2f/src/frontend/soblogitsgood/soblogitsgood/templates/analysis.mako'
_template_uri='/analysis.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['more_head_tags']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 2
    ns = runtime.Namespace(u'helper', context._clean_inheritance_tokens(), templateuri=u'/helper.mako', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, u'helper')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/sbig.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        helper = _mako_get_namespace(context, 'helper')
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n')
        # SOURCE LINE 247
        __M_writer(u'\n\n<table width="100%" cellspacing="0">\n<tr>\n  <td class="leftcorner" style="background-image:\n      url(\'../images/goodcorner.png\');">\n      <p />\n  </td>\n  <td id="overview_header" class="graphheader">\n    Overview [-]\n  </td>\n  <td class="rightcorner" style="background-image: \n      url(\'../images/rgoodcorner.png\');">\n      <p />\n  </td>\n</tr>\n<tr>\n  <td colspan="3">\n    <div id="overview_graphs">\n      <table>\n        <tr>\n          <td>\n            <div id="pie" style="width: 300px; height: 250px; margin: 0 auto"></div>\n          </td>\n          <td class="tagcloud">\n            ')
        # SOURCE LINE 272
        __M_writer(escape(helper.tagCloud(c.goodTerms, c.badTerms)))
        __M_writer(u'\n          </td>\n        </tr>\n      </table>\n    </div>\n  </td>\n</tr>\n<tr>\n  <td class="leftcorner" style="background-image:\n      url(\'../images/goodcorner.png\');">\n      <p />\n  </td>\n  <td id="stats_header" class="graphheader">\n    Statistics [-]\n  </td>\n  <td class="rightcorner" style="background-image: \n      url(\'../images/rgoodcorner.png\');">\n      <p />\n  </td>\n</tr>\n<tr>\n  <td colspan="3">\n  <div id="stats_body">\n      <p align="center">\n      Verdict: ')
        # SOURCE LINE 296
        __M_writer(escape(c.verdict))
        __M_writer(u'\n      </p>\n      <div id="stats_graphs">\n        <div id="line" style="width: 700px; height: 400px; margin: 0 auto"></div>\n      </div>\n  </div>\n  </td>\n</tr>\n</table>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_more_head_tags(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        helper = _mako_get_namespace(context, 'helper')
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n  <script type="text/javascript" \n    src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">\n  </script>\n  <script type="text/javascript" src="scripts/highcharts.js"></script>\n\n<script type="text/javascript">\nvar piechart;\n$(document).ready(function() {\n  piechart = new Highcharts.Chart({\n    chart: {\n      renderTo: \'pie\',\n      margin: [0,0,0,0]\n    },\n    title: {\n      text: null,\n    },\n    tooltip: {\n      formatter: function() {\n        return \'<b>\'+ this.point.name +\'</b>: \'+ this.y +\' results\';\n      }\n    },\n    plotOptions: {\n      pie: {\n        borderColor: \'#FFFFFF\',\n        borderWidth: 3,\n        cursor: \'pointer\',\n        dataLabels: {\n            distance: -35,\n            enabled: false,\n            formatter: function() {\n              if (this.percentage > 10) return this.point.name;\n            },\n            style: {\n              font: \'13px Trebuchet MS, Verdana, sans-serif\',\n            }\n        }\n      }\n    },\n    legend: {\n      enabled: false,\n      layout: \'vertical\',\n      style: {\n        left: \'auto\',\n        bottom: \'auto\',\n        right: \'0px\',\n        top: \'0px\'\n      }\n    },\n    series: [{\n      type: \'pie\',\n      name: \'Good vs. Bad\',\n      data: [\n        {\n          name: \'Good\',  \n          y: ')
        # SOURCE LINE 59
        __M_writer(escape(len(c.goodResults)))
        __M_writer(u",\n          color: '#49BD43'\n        },\n        {\n          name: 'Mediocre',  \n          y: ")
        # SOURCE LINE 64
        __M_writer(escape(len(c.neutralResults)))
        __M_writer(u",\n          color: '#a1884b'\n        },\n        {\n          name: 'Bad',\n          y: ")
        # SOURCE LINE 69
        __M_writer(escape(len(c.badResults)))
        __M_writer(u",\n          color: '#F95353'\n        },\n      ]\n    }]\n  });\n});\n\nvar linechart;\n$(document).ready(function() {\n    linechart = new Highcharts.Chart({\n        chart: {\n            renderTo: 'line',\n            defaultSeriesType: 'line',\n            marginRight: 30,\n            marginBottom: 75\n        },\n        title: {\n            text: null,\n            style: {\n                color: '#F95353',\n            },\n            x: -20 //center\n        },\n        yAxis: {\n            gridLineColor: '#FED9D8',\n            allowDecimals: false,\n            min: 0,\n            title: {\n                text: 'Number of Reviews',\n                style: {\n                    color: '#49BD43',\n                }\n            },\n            labels: {\n                style: {\n                    color: '#F95353',\n                }\n            }\n        },\n        xAxis: {\n            tickColor: '#FCA2A2',\n            lineColor: '#FCA2A2',\n            title: {\n                text: 'Sentiment Score',\n                style: {\n                    color: '#49BD43',\n                }\n            },\n            plotLines: [{\n                dashStyle: 'dash',\n                value: ")
        # SOURCE LINE 120
        __M_writer(escape(c.mean*100))
        __M_writer(u",\n                width: 1.5,\n                color: '#FCA2A2',\n                zIndex: 5,\n                label: {\n                    style: {\n                        color: '#F95353',\n                        fontWeight: 'bold',\n                    },\n                    text: 'Average: '+ Math.round(")
        # SOURCE LINE 129
        __M_writer(escape(c.mean))
        __M_writer(u"*100)+ '%',\n                }\n            }],\n            labels: {\n                formatter: function() {\n                    return this.value + '%';\n                },\n                style: {\n                    color: '#F95353',\n                }\n            }\n        },\n        tooltip: {\n            formatter: function() {\n                return this.x +'%: '+ this.y + ' reviews';\n            }\n        },\n        legend: {\n            enabled: false,\n            layout: 'vertical',\n            align: 'right',\n            verticalAlign: 'top',\n            x: -10,\n            y: 100,\n            borderWidth: 0\n        },\n        series: [\n            {name: 'Results', color: '#363636', pointInterval: 10, data:\n                    ")
        # SOURCE LINE 157
        __M_writer(escape(helper.sort(c.results)))
        __M_writer(u'},\n        ]\n        \n    });\n});\n    \n$(document).ready(function(){\n  //$("#stats_body").hide();\n  \n  $("#overview_header").toggle(function(){\n    $("#overview_graphs").slideDown();\n    $("#overview_header").html("Overview [-]")\n  }, function() {\n    $("#overview_graphs").slideUp();\n    $("#overview_header").html("Overview [+]")\n  });\n\n  $("#stats_header").toggle(function(){\n    $("#stats_body").slideDown();\n    $("#stats_header").html("Statistics [-]")\n  }, function() {\n    $("#stats_body").slideUp();\n    $("#stats_header").html("Statistics [+]")\n  });\n\n  $("#narrow").bind("click", function(){\n    params = new Array();\n    params["query"] = "')
        # SOURCE LINE 184
        __M_writer(escape(c.query))
        __M_writer(u'";\n    params["narrow"] = true;\n    // Build restrictions\n    products = new Array();\n    sources = new Array();\n\n    $(".sourcecheck").each(function() {\n        if($(this).is(":checked")) {\n            sources.push($(this).attr("id"));\n        }\n    });\n\n    $(".prodcheck").each(function() {\n        if($(this).is(":checked")) {\n            products.push($(this).attr("id"));\n        }\n    });\n\n    params["products"] = products;\n    params["sources"] = sources;\n    post_to_url("analysis", params)\n  });\n\n  $(".sourcecheck").live("click", function() {\n    source = $(this).attr("id").substring(8);\n    if($(this).is(":checked")) {\n        $("#cat" + source).slideDown();\n    } else {\n        $("#cat" + source).slideUp();\n    }\n  });\n\n  $(".sourcecheck").each(function() {\n    source = $(this).attr("id").substring(8);\n    if($(this).is(":checked")) {\n        $("#cat" + source).show();\n    } else {\n        $("#cat" + source).hide();\n    }\n  });\n});\n\nfunction post_to_url(path, params) {\n    // The rest of this code assumes you are not using a library.\n    // It can be made less wordy if you use one.\n    var form = document.createElement("form");\n    form.setAttribute("method", "post");\n    form.setAttribute("action", path);\n\n    for(var key in params) {\n        var hiddenField = document.createElement("input");\n        hiddenField.setAttribute("type", "hidden");\n        hiddenField.setAttribute("name", key);\n        hiddenField.setAttribute("value", params[key]);\n\n        form.appendChild(hiddenField);\n    }\n\n    document.body.appendChild(form);    // Not entirely sure if this is necessary\n    form.submit();\n}\n\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


