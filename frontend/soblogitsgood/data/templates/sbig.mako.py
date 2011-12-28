# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1306272482.543685
_template_filename=u'/home/god/Dropbox/f2f/src/frontend/soblogitsgood/soblogitsgood/templates/sbig.mako'
_template_uri=u'/sbig.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['fix', 'productfix']


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
    return runtime._inherit_from(context, u'/sbig_base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        c = context.get('c', UNDEFINED)
        def fix(s):
            return render_fix(context.locals_(__M_locals),s)
        hasattr = context.get('hasattr', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n')
        # SOURCE LINE 14
        __M_writer(u'\n\n')
        # SOURCE LINE 18
        __M_writer(u'\n\n<br/>\n<table width="1000">\n  <tr>\n  <td>\n  </td>\n  <td>\n      ')
        # SOURCE LINE 26
        __M_writer(escape(self.search_box()))
        __M_writer(u'\n      <br />\n      <br />\n  </td>\n  </tr>\n  <tr>\n')
        # SOURCE LINE 32
        if hasattr(c, "query"):
            # SOURCE LINE 33
            __M_writer(u'      <td class="sidebar">\n        <ul class="views">\n\n        <li>\n          <span class="icon" style="background-image:\n              url(\'images/list.png\');"></span>\n')
            # SOURCE LINE 39
            if c.service == "search":
                # SOURCE LINE 40
                __M_writer(u'          <span class="modePicked">List</span>\n')
                # SOURCE LINE 41
            else:
                # SOURCE LINE 42
                __M_writer(u'          <a href="search?query=')
                __M_writer(escape(c.query.replace(" ", "+")))
                __M_writer(u'">List</a>\n')
                pass
            # SOURCE LINE 44
            __M_writer(u'        </li>\n\n        <li>\n          <span class="icon" style="background-image:\n              url(\'images/polarize.png\');"></span>\n')
            # SOURCE LINE 49
            if c.service == "polarize":
                # SOURCE LINE 50
                __M_writer(u'          <span class="modePicked">Polarize</span>\n')
                # SOURCE LINE 51
            else:
                # SOURCE LINE 52
                __M_writer(u'          <a href="polarize?query=')
                __M_writer(escape(c.query.replace(" ", "+")))
                __M_writer(u'">Polarize</a>\n')
                pass
            # SOURCE LINE 54
            __M_writer(u'        </li>\n\n        <li>\n          <span class="icon" style="background-image:\n              url(\'images/analysis.png\');"></span>\n')
            # SOURCE LINE 59
            if c.service == "analysis":
                # SOURCE LINE 60
                __M_writer(u'          <span class="modePicked">Analysis</span>\n')
                # SOURCE LINE 61
            else:
                # SOURCE LINE 62
                __M_writer(u'          <a href="analysis?query=')
                __M_writer(escape(c.query.replace(" ", "+")))
                __M_writer(u'">Analysis</a>\n')
                pass
            # SOURCE LINE 64
            __M_writer(u'        </li>\n        </ul>\n\n        <div id="categories">\n        <p class="cattitle">\n          Categories\n           \n')
            # SOURCE LINE 71
            if c.service == "analysis":
                # SOURCE LINE 72
                __M_writer(u'          <input id="narrow" value="Narrow" type="submit"><br>\n')
                pass
            # SOURCE LINE 74
            __M_writer(u'        </p>\n')
            # SOURCE LINE 75
            if c.service == "analysis":
                # SOURCE LINE 76
                for source, products in c.categories.items():
                    # SOURCE LINE 77
                    __M_writer(u'            <span class="sourcetitle">\n')
                    # SOURCE LINE 78
                    if c.narrowparsers is None or fix(source) in c.narrowparsers:
                        # SOURCE LINE 79
                        __M_writer(u'                <input class="sourcecheck" checked="true" type="checkbox" id="category')
                        __M_writer(escape(source))
                        __M_writer(u'">')
                        __M_writer(escape(source))
                        __M_writer(u'<br>\n')
                        # SOURCE LINE 80
                    else:
                        # SOURCE LINE 81
                        __M_writer(u'                <input class="sourcecheck" type="checkbox" id="category')
                        __M_writer(escape(source))
                        __M_writer(u'">')
                        __M_writer(escape(source))
                        __M_writer(u'<br>\n')
                        pass
                    # SOURCE LINE 83
                    __M_writer(u'            </span>\n            <ul class="categories" id="cat')
                    # SOURCE LINE 84
                    __M_writer(escape(source))
                    __M_writer(u'">\n')
                    # SOURCE LINE 85
                    for product in products:
                        # SOURCE LINE 86
                        __M_writer(u'                <li id="prod')
                        __M_writer(escape(fix(product)))
                        __M_writer(u'">\n')
                        # SOURCE LINE 87
                        if c.narrowproducts is None or fix(product) in c.narrowproducts:
                            # SOURCE LINE 88
                            __M_writer(u'                    <input class="prodcheck" checked="true" type="checkbox" id="product')
                            __M_writer(escape(fix(product)))
                            __M_writer(u'">')
                            __M_writer(escape(context.write(product)))
                            __M_writer(u'\n')
                            # SOURCE LINE 89
                        else:
                            # SOURCE LINE 90
                            __M_writer(u'                    <input class="prodcheck" type="checkbox" id="product')
                            __M_writer(escape(fix(product)))
                            __M_writer(u'">')
                            __M_writer(escape(context.write(product)))
                            __M_writer(u'\n')
                            pass
                        # SOURCE LINE 92
                        __M_writer(u'                </li>\n')
                        pass
                    # SOURCE LINE 94
                    __M_writer(u'            </ul>\n')
                    pass
                pass
            # SOURCE LINE 97
            __M_writer(u'        </div>\n      </td>\n')
            pass
        # SOURCE LINE 100
        __M_writer(u'    <td class="content">\n      ')
        # SOURCE LINE 101
        __M_writer(escape(next.body()))
        __M_writer(u'\n    </td>\n  </tr>\n</table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_fix(context,s):
    context.caller_stack._push_frame()
    try:
        def productfix(char):
            return render_productfix(context,char)
        __M_writer = context.writer()
        # SOURCE LINE 16

        return "".join([productfix(c) for c in s])
        
        
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_productfix(context,char):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 5

        if char.isalnum():
          return char
        elif char == "-" or char == "_":
          return char
        elif char.isspace():
          return "_"
        else:
          return "_"
        
        
        return ''
    finally:
        context.caller_stack._pop_frame()


