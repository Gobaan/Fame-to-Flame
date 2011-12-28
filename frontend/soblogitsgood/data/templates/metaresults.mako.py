# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1299985621.2269681
_template_filename='/home/max/school/fydp/src/frontend/soblogitsgood/soblogitsgood/templates/metaresults.mako'
_template_uri='/metaresults.mako'
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
        # SOURCE LINE 87
        __M_writer(u'\n\n<div id="allresults">\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_more_head_tags(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n  <script type="text/javascript"\n  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>\n\n  <script type="text/javascript">\n    $.fn.exists = function() {\n        return $(this).length !== 0;\n    }\n\n    timerid = 0\n\n    function stopTimer()\n    {\n        clearInterval(timerid)\n    }\n\n    function loadResults()\n    {\n      $.ajax({async: false,\n              url:  "getasyncresults",\n              type: "POST",\n              dataType: "xml",\n              data: { query: "')
        # SOURCE LINE 26
        __M_writer(escape(c.query))
        __M_writer(u'" },\n              success: function(data){\n                $(data).find("stop").each(function(){\n                    stopTimer();\n                });\n                $(data).find("result").each(function(){\n                    source = $(this).find("source").text();\n                    product = $(this).find("product").text();\n                    if(! $("#results" + source).exists()) {\n                        $("#allresults").append("<div id=\\"results" + source +\n                            "\\"><h2>" + source + "</h2></div>\\n");\n                        $("#categories").append(\n                            "<input checked=\\"true\\" type=\\"checkbox\\"" +\n                            "id=\\"category" + source + "\\">" +\n                            source +\n                            "<ul class=\\"categories\\" id=\\"cat" + source + "\\">" +\n                            "</ul>");\n                        $("#category" + source).live("click", function() {\n                            source = $(this).attr("id").substring(8);\n                            if($(this).is(":checked")) {\n                                $("#results" + source).show();\n                                $("#cat" + source + " input").attr("checked", "true");\n                            } else {\n                                $("#results" + source).hide();\n                                $("#cat" + source + " input").attr("checked", "false");\n                            }\n                        });\n                    }\n                    prod = $(this).find("cssproduct").text();\n\n                    if(! $("#prod" + prod).exists()) {\n                        $("#cat" + source).append(\n                            "<li id=\\"prod" + prod + "\\">" +\n                            "<input checked=\\"true\\" type=\\"checkbox\\"" +\n                            "id=\\"product" + prod + "\\">" +\n                            product +\n                            "</li>");\n\n                        $("#product" + prod).live("click", function() {\n                            prod = $(this).attr("id").substring(7);\n                            if($(this).is(":checked")) {\n                                $(".prod" + prod).show();\n                            } else {\n                                $(".prod" + prod).hide();\n                            }\n                        });\n                    }\n\n                    $("#results" + source).append("<div class=\\"prod" + prod + "\\">" +\n                            $(this).find("content").text() + "</div>");\n                });\n              }\n        });\n    }\n\n    $(document).ready(function() {\n      timerid = setInterval("loadResults()", 3000);\n      loadResults();\n      setTimeout("stopTimer()", 30000);\n    });\n  </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


