# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1306272904.88985
_template_filename='/home/god/Dropbox/f2f/src/frontend/soblogitsgood/soblogitsgood/templates/noresults.mako'
_template_uri='/noresults.mako'
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
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 75
        __M_writer(u'\n\n<br/>\n<br/>\n<center>\nSorry, your search <b>')
        # SOURCE LINE 80
        __M_writer(escape(c.query))
        __M_writer(u'</b> had no results.\n</center>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_more_head_tags(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n<script type="text/javascript" \n  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">\n</script>\n\n<script type="text/javascript">\n\nfunction post_to_url(path, params) {\n    // The rest of this code assumes you are not using a library.\n    // It can be made less wordy if you use one.\n    var form = document.createElement("form");\n    form.setAttribute("method", "post");\n    form.setAttribute("action", path);\n\n    for(var key in params) {\n        var hiddenField = document.createElement("input");\n        hiddenField.setAttribute("type", "hidden");\n        hiddenField.setAttribute("name", key);\n        hiddenField.setAttribute("value", params[key]);\n\n        form.appendChild(hiddenField);\n    }\n\n    document.body.appendChild(form);    // Not entirely sure if this is necessary\n    form.submit();\n}\n\n$(document).ready(function() {\n  $("#narrow").bind("click", function(){\n    params = new Array();\n    params["query"] = "')
        # SOURCE LINE 33
        __M_writer(escape(c.query))
        __M_writer(u'";\n    params["narrow"] = true;\n    // Build restrictions\n    products = new Array();\n    sources = new Array();\n\n    $(".sourcecheck").each(function() {\n        if($(this).is(":checked")) {\n            sources.push($(this).attr("id"));\n        }\n    });\n\n    $(".prodcheck").each(function() {\n        if($(this).is(":checked")) {\n            products.push($(this).attr("id"));\n        }\n    });\n\n    params["products"] = products;\n    params["sources"] = sources;\n    post_to_url("analysis", params)\n  });\n\n  $(".sourcecheck").live("click", function() {\n    source = $(this).attr("id").substring(8);\n    if($(this).is(":checked")) {\n        $("#cat" + source).show();\n    } else {\n        $("#cat" + source).hide();\n    }\n  });\n\n  $(".sourcecheck").each(function() {\n    source = $(this).attr("id").substring(8);\n    if($(this).is(":checked")) {\n        $("#cat" + source).show();\n    } else {\n        $("#cat" + source).hide();\n    }\n  });\n});\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


