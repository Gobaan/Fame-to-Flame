# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1306272591.701375
_template_filename='/home/god/Dropbox/f2f/src/frontend/soblogitsgood/soblogitsgood/templates/custom.mako'
_template_uri='/custom.mako'
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
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n')
        # SOURCE LINE 131
        __M_writer(u'\n\n<div width="100%" align="center">\n')
        # SOURCE LINE 135
        __M_writer(u'  <div class="slider"></div>\n  <span class="slider-display">\n    Viewing 0% to 100%\n  </span>\n  <br />\n</div>\n<br/>\n\n<div id="allresults"></div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_more_head_tags(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n  <link rel="stylesheet" type="text/css" href="styles/custom-theme/jquery-ui-1.8.10.custom.css" />\n\n  <script type="text/javascript"\n  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>\n  <script type="text/javascript" src="scripts/jquery-ui-1.8.2.custom.min.js"></script>\n\n  <script type="text/javascript">\n  $(document).ready(function() {\n    $(".slider").slider({\n        range: true,\n        min: 0,\n        max: 1,\n        step: 0.1,\n        values: [0, 1],\n        slide: function(event, ui) {\n            $(".slider-display").html("Viewing "\n                + ui.values[0]*100 + "% to " + ui.values[1]*100 + "%");\n            $(".item").each(function(){\n                sent = $(this).attr("sentiment");\n                bot = ui.values[0];\n                top = ui.values[1];\n                if(sent >= bot && sent <= top) {\n                    $(this).show();\n                } else {\n                    $(this).hide();\n                }\n            });\n        }\n    });\n  });\n</script>\n\n<script type="text/javascript">\n$.fn.exists = function() {\n    return $(this).length !== 0;\n}\n\ntimerid = 0\n\nfunction stopTimer()\n{\n    clearInterval(timerid)\n}\n\nfunction loadResults()\n{\n    $.ajax({async: false,\n            url:  "getasyncresults",\n            type: "POST",\n            dataType: "xml",\n            data: { query: "')
        # SOURCE LINE 55
        __M_writer(escape(c.query))
        __M_writer(u'" },\n            success: function(data){\n            $(data).find("stop").each(function(){\n                stopTimer();\n                });\n            $(data).find("result").each(function(){\n                source = $(this).find("source").text();\n                product = $(this).find("product").text();\n                cssprod = $(this).find("cssproduct").text();\n                sentiment = $(this).find("sentiment").text();\n\n                if(! $("#category" + source).exists()) {\n                $("#categories").append(\n                    "<input checked=\\"true\\" type=\\"checkbox\\"" +\n                    "id=\\"category" + source + "\\"><span class=\'sourcetitle\'>" +\n                    source + "<br>" +\n                    "</span><ul class=\\"categories\\" id=\\"cat" + source + "\\">" +\n                    "</ul>");\n                $("#category" + source).live("click", function() {\n                    source = $(this).attr("id").substring(8);\n                    if($(this).is(":checked")) {\n                        $(".item" + source).show();\n                        $("#cat" + source).slideDown();\n                    } else {\n                        $(".item" + source).hide();\n                        $("#cat" + source).slideUp();\n                    }\n                    });\n                }\n\n                if(! $("#product" + cssprod).exists()) {\n                    $("#cat" + source).append(\n                            "<li>" +\n                            "<input checked=\\"true\\" type=\\"checkbox\\"" +\n                            "id=\\"product" + cssprod + "\\">" +\n                            product +\n                            "</li>");\n\n                    $("#product" + cssprod).live("click", function() {\n                            cssprod = $(this).attr("id").substring(7);\n                            if($(this).is(":checked")) {\n                            $(".prod" + cssprod).show();\n                            } else {\n                            $(".prod" + cssprod).hide();\n                            }\n                            });\n                }\n\n                $("#allresults").append(\n                        "<div class=\\"item\\" sentiment=\\"" + sentiment + "\\">" +\n                        "<div class=\\"item" + source + "\\">" +\n                        "<div class=\\"prod" + cssprod + "\\">" +\n                        $(this).find("content").text() +\n                        "</div></div>");\n            });\n\n            $(".item").each(function(){\n                sent = $(this).attr("sentiment");\n                bot = $(".slider").slider("values")[0];\n                top = $(".slider").slider("values")[1];\n                if(sent >= bot && sent <= top) {\n                    $(this).show();\n                } else {\n                    $(this).hide();\n                }\n            });\n            }\n    });\n}\n\n$(document).ready(function() {\n        timerid = setInterval("loadResults()", 3000);\n        loadResults();\n        setTimeout("stopTimer()", 30000);\n        });\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


