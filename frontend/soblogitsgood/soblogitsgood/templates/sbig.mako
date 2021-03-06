## This template outlines the main page layout

<%inherit file="/sbig_base.mako" />

<%def name="productfix(char)"><%
  if char.isalnum():
    return char
  elif char == "-" or char == "_":
    return char
  elif char.isspace():
    return "_"
  else:
    return "_"
%></%def>

<%def name="fix(s)"><%
  return "".join([productfix(c) for c in s])
%></%def>

<br/>
<table width="1000">
  <tr>
  <td>
  </td>
  <td>
      ${self.search_box()}
      <br />
      <br />
  </td>
  </tr>
  <tr>
    % if hasattr(c, "query"):
      <td class="sidebar">
        <ul class="views">

        <li>
          <span class="icon" style="background-image:
              url('images/list.png');"></span>
        % if c.service == "search":
          <span class="modePicked">List</span>
        % else:
          <a href="search?query=${c.query.replace(" ", "+")}">List</a>
        % endif
        </li>

        <li>
          <span class="icon" style="background-image:
              url('images/polarize.png');"></span>
        % if c.service == "polarize":
          <span class="modePicked">Polarize</span>
        % else:
          <a href="polarize?query=${c.query.replace(" ", "+")}">Polarize</a>
        % endif
        </li>

        <li>
          <span class="icon" style="background-image:
              url('images/analysis.png');"></span>
        % if c.service == "analysis":
          <span class="modePicked">Analysis</span>
        % else:
          <a href="analysis?query=${c.query.replace(" ", "+")}">Analysis</a>
        % endif
        </li>
        </ul>

        <div id="categories">
        <p class="cattitle">
          Categories
           
        % if c.service == "analysis":
          <input id="narrow" value="Narrow" type="submit"><br>
        % endif
        </p>
        % if c.service == "analysis":
        % for source, products in c.categories.items():
            <span class="sourcetitle">
            % if c.narrowparsers is None or fix(source) in c.narrowparsers:
                <input class="sourcecheck" checked="true" type="checkbox" id="category${source}">${source}<br>
            % else:
                <input class="sourcecheck" type="checkbox" id="category${source}">${source}<br>
            % endif
            </span>
            <ul class="categories" id="cat${source}">
            % for product in products:
                <li id="prod${fix(product)}">
                % if c.narrowproducts is None or fix(product) in c.narrowproducts:
                    <input class="prodcheck" checked="true" type="checkbox" id="product${fix(product)}">${context.write(product)}
                % else:
                    <input class="prodcheck" type="checkbox" id="product${fix(product)}">${context.write(product)}
                % endif
                </li>
            % endfor
            </ul>
        % endfor
        % endif
        </div>
      </td>
    % endif
    <td class="content">
      ${next.body()}
    </td>
  </tr>
</table>
