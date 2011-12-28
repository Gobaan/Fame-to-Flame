# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1306272482.479773
_template_filename=u'/home/god/Dropbox/f2f/src/frontend/soblogitsgood/soblogitsgood/templates/helper.mako'
_template_uri=u'/helper.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['normalize', 'sort', 'tagCloud', 'printResult', 'boldTerm', 'summarize']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 20
        __M_writer(u'\n\n')
        # SOURCE LINE 36
        __M_writer(u'\n\n')
        # SOURCE LINE 73
        __M_writer(u'\n\n')
        # SOURCE LINE 89
        __M_writer(u'\n\n')
        # SOURCE LINE 121
        __M_writer(u'\n\n')
        # SOURCE LINE 148
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_normalize(context,a):
    context.caller_stack._push_frame()
    try:
        max = context.get('max', UNDEFINED)
        min = context.get('min', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n  ')
        # SOURCE LINE 3

        if not a:
          return []
        
        # Find the range of values
        best = a[0][1]
        worst = best
        for i in a:
          best = max(best, i[1])
          worst = min(worst, i[1])
        
        # Normalize values
        if best == worst:
          return [(k.lower(), 0.5) for k, v in a]
        else:
          return [(k.lower(), (v - worst) / (best - worst)) for k, v in a]
          
        
        # SOURCE LINE 19
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_sort(context,results):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        range = context.get('range', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 125
        __M_writer(u'\n  ')
        # SOURCE LINE 126

        SPAN = 100
        BUCKET = 10
        
        axis = range(0, SPAN+BUCKET, BUCKET)
        axis = [str(val)+'%' for val in axis]
        buckets = [0] * (SPAN/BUCKET + 1)
        
        for res in results:
          # convert probability in to percentage and round down
          # e.g. 0.98 -> 98 -> 198 then rounds down by BUCKET; 98/20 = 10
          if res['sentiment'] > 1.0:
            sent = 1.0
          elif res['sentiment'] < 0.0:
            sent = 0.0
          else:
            sent = res['sentiment']
          i = int(sent * 100)/BUCKET
          buckets[i] += 1
        
        context.write(str(buckets))
        
        
        # SOURCE LINE 147
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tagCloud(context,good,bad):
    context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 91
        __M_writer(u'\n  ')
        # SOURCE LINE 92

  # Constants
        BIG = 150
        SMALL = 70
        RNG = BIG - SMALL
        
        good = self.normalize(good)
        bad = self.normalize(bad)
        
        terms = [(k, v, True) for k, v in good] + [(k, v, False) for k, v in bad]
        
        if not terms:
          return ""
        
        # Sort alphabetically
        terms.sort()
        
        # Write the tag cloud
        for term in terms:
          if term[2]:
            context.write("<span class=\"good\">")
          else:
            context.write("<span class=\"bad\">")
        
          context.write("<span style=\"font-size:%d%%\">" % (term[1] * RNG + SMALL))
        
          context.write(term[0])
          context.write("&nbsp;&nbsp;</span></span> ")
        
        
        # SOURCE LINE 120
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_printResult(context,r):
    context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        def summarize(text):
            return render_summarize(context,text)
        def boldTerm(text):
            return render_boldTerm(context,text)
        __M_writer = context.writer()
        # SOURCE LINE 75
        __M_writer(u'\n  <h3 class="resultLink">\n    <a href="')
        # SOURCE LINE 77
        __M_writer(escape(r['link']))
        __M_writer(u'">')
        __M_writer(escape(boldTerm(r['product'])))
        __M_writer(u' - ')
        __M_writer(escape(boldTerm(r['title'])))
        __M_writer(u'</a><br/>\n  </h3>\n  <p class="result">\n')
        # SOURCE LINE 80
        if r['sentiment'] >= 0.7:
            # SOURCE LINE 81
            __M_writer(u'      <span class="good">Sentiment: ')
            __M_writer(escape(int(r['sentiment'] * 100)))
            __M_writer(u'%</span><br/>\n')
            # SOURCE LINE 82
        elif r['sentiment'] < 0.6:
            # SOURCE LINE 83
            __M_writer(u'      <span class="bad">Sentiment: ')
            __M_writer(escape(int(r['sentiment'] * 100)))
            __M_writer(u'%</span><br/>\n')
            # SOURCE LINE 84
        else:
            # SOURCE LINE 85
            __M_writer(u'      <span class="neutral">Sentiment: ')
            __M_writer(escape(int(r['sentiment'] * 100)))
            __M_writer(u'%</span><br/>\n')
            pass
        # SOURCE LINE 87
        __M_writer(u'    ')
        __M_writer(escape(boldTerm(summarize(r['content']))))
        __M_writer(u'\n  </p>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_boldTerm(context,text):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 22
        __M_writer(u'\n  ')
        # SOURCE LINE 23

        out = text
        index = -8
        while (True):
          index = out.lower().find(c.query.lower(), index + 8)
          if index >= 0:
            out = "%s<b>%s</b>%s" % (out[:index],
                                     out[index:index + len(c.query)],
                                     out[index + len(c.query):])
          else:
            break
        context.write(out)
          
        
        # SOURCE LINE 35
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_summarize(context,text):
    context.caller_stack._push_frame()
    try:
        max = context.get('max', UNDEFINED)
        c = context.get('c', UNDEFINED)
        abs = context.get('abs', UNDEFINED)
        len = context.get('len', UNDEFINED)
        min = context.get('min', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 38
        __M_writer(u'\n  ')
        # SOURCE LINE 39

        BACK = 50
        LENGTH = 400
        CHECK = 25
        index = text.lower().find(c.query.lower())
        if index < 0:
          left = 0
        # Find a chunk of text around the search term
        left = max(0, index - BACK)
        right = min(len(text), left + LENGTH)
        
        # Find if the ranges are close to periods
        lcheck = max(0, left - CHECK)
        rcheck = right - CHECK
        
        lstop = text.find(".", lcheck)
        rstop = text.find(".", rcheck)
        
        prefix = "..."
        postfix = "..."
        
        if abs(left - lstop) <= CHECK:
          left = lstop + 1
          prefix = ""
        if abs(right - rstop) <= CHECK:
          right = rstop + 1
          postfix = ""
        if left == 0:
          prefix = ""
        if right == len(text):
          postfix = ""
        
        return prefix + text[left:right].strip() + postfix# + "~%d, %d" % (left, right)
          
        
        # SOURCE LINE 72
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


