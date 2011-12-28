## This file has just the search box functionality

<%inherit file="/base.mako" />

<%def name="head_tags()">
  % if hasattr(c, "title"):
    <title>${c.title}</title>
  % else:
    <title>Fame to Flame</title>
  % endif
  <link rel="stylesheet" type="text/css" href="styles/style.css" />

  <%
  try:
    self.more_head_tags()
  except AttributeError:
    pass
  %>
</%def>

<%def name="search_box()">
  <center>
  <a href="/">
  <img src="images/logo.png" style="border: 0px;"/>
  </a>
  <br />
  <br />
  <form name="form" action="${c.service}" method="GET">
    % if hasattr(c, "query"):
      <input name="query" type="text" size="40" value="${c.query}"/>
    % else:
      <input name="query" type="text" size="40" />
    % endif
    <input type="submit" value="Search" />
  </form>
  </center>
</%def>

${next.body()}
