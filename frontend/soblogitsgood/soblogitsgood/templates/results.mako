<%inherit file="/sbig.mako" />
<%namespace name="helper" file="/helper.mako" />

<%def name="more_head_tags()">
  <script type="text/javascript"
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>

  <script type="text/javascript">
    $(document).ready(function() {
      $(":button").bind('click', function() {
        guid = this.attributes['guid'].value;
        $.ajax({ url: "feedback",
                 type: "POST",
                 data: { guid: this.attributes['guid'].value,
                         type: this.attributes['name'].value}
              });
      });
    });
  </script>
</%def>

<%def name="printResultWithFeedback(r)">
  <table><tr><td>
    <input type="button" name="up" class="up" value="" guid="${r['guid']}">
    <br />
    <input type="button" name="down" class="down" value="" guid="${r['guid']}">
  </td><td>
   ${helper.printResult(r)}
  </td></tr></table>
</%def>

% for result in c.results:
  ## ${helper.printResult(result)}
  ${printResultWithFeedback(result)}
% endfor

## Pagination
<center>
  <%
    # Constants
    RNG = 4
    TOTAL = RNG + RNG + 1
    basestr = "<a href=\"search?query=%s&start=%d\">%d</a> "
    urlquery = c.query.replace(" ", "+")

    # Find page values
    currpage = c.results.start/10
    startpage = max(0, currpage - RNG)
    endpage = min(c.results.numFound/10, currpage + TOTAL - (currpage - startpage))
    startpage = max(0, min(startpage, currpage - (TOTAL - endpage + currpage)))

    if endpage == 0:
      return

    # Link to page 1 if far away
    if startpage != 0:
      context.write(basestr % (c.query, 0, 1))
      if startpage != 1:
        context.write("... ")

    # Page links
    for i in xrange(startpage, endpage + 1):
      context.write(basestr % (urlquery, 10 * i, i + 1))

    # Link to last page if far away
    if endpage != c.results.numFound/10:
      if endpage != c.results.numFound/10 - 1:
        context.write("... ")
      last = c.results.numFound/10
      context.write(basestr % (urlquery, last*10, last + 1))
  %>
</center>
