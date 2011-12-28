# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1306272475.897076
_template_filename=u'/home/god/Dropbox/f2f/src/frontend/soblogitsgood/soblogitsgood/templates/sbig_base.mako'
_template_uri=u'/sbig_base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['search_box', 'head_tags']


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
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n')
        # SOURCE LINE 19
        __M_writer(u'\n\n')
        # SOURCE LINE 37
        __M_writer(u'\n\n')
        # SOURCE LINE 39
        __M_writer(escape(next.body()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_search_box(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        hasattr = context.get('hasattr', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 21
        __M_writer(u'\n  <center>\n  <a href="/">\n  <img src="images/logo.png" style="border: 0px;"/>\n  </a>\n  <br />\n  <br />\n  <form name="form" action="')
        # SOURCE LINE 28
        __M_writer(escape(c.service))
        __M_writer(u'" method="GET">\n')
        # SOURCE LINE 29
        if hasattr(c, "query"):
            # SOURCE LINE 30
            __M_writer(u'      <input name="query" type="text" size="40" value="')
            __M_writer(escape(c.query))
            __M_writer(u'"/>\n')
            # SOURCE LINE 31
        else:
            # SOURCE LINE 32
            __M_writer(u'      <input name="query" type="text" size="40" />\n')
            pass
        # SOURCE LINE 34
        __M_writer(u'    <input type="submit" value="Search" />\n  </form>\n  </center>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        AttributeError = context.get('AttributeError', UNDEFINED)
        self = context.get('self', UNDEFINED)
        hasattr = context.get('hasattr', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 5
        __M_writer(u'\n')
        # SOURCE LINE 6
        if hasattr(c, "title"):
            # SOURCE LINE 7
            __M_writer(u'    <title>')
            __M_writer(escape(c.title))
            __M_writer(u'</title>\n')
            # SOURCE LINE 8
        else:
            # SOURCE LINE 9
            __M_writer(u'    <title>Fame to Flame</title>\n')
            pass
        # SOURCE LINE 11
        __M_writer(u'  <link rel="stylesheet" type="text/css" href="styles/style.css" />\n\n  ')
        # SOURCE LINE 13

        try:
          self.more_head_tags()
        except AttributeError:
          pass
        
        
        # SOURCE LINE 18
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


