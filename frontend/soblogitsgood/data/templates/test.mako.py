# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1299462280.04706
_template_filename='/home/max/school/fydp/src/frontend/soblogitsgood/soblogitsgood/templates/test.mako'
_template_uri='/test.mako'
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
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/sbig.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 24
        __M_writer(u'\n\n<div id="testing">\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_more_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n  <script type="text/javascript"\n  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>\n\n  <script type="text/javascript">\n    $(document).ready(function() {\n      $("#testing").append("abcd");\n\n      $.ajax({async: false,\n              url:  "testajax",\n              type: "POST",\n              dataType: "xml",\n              success: function(data){\n                    $(data).find("result").each(function(){\n                        alert($(this).text())\n                        $("#testing").append($(this).find("source").text());\n                    });\n              }\n        });\n    });\n  </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


