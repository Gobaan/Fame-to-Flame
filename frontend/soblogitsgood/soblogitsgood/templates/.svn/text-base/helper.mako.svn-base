## Add <b> tags around the search term in given text
<%def name="normalize(a)">
  <%
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
  %>
</%def>

<%def name="boldTerm(text)">
  <%
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
  %>
</%def>

<%def name="summarize(text)">
  <%
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
  %>
</%def>

<%def name="printResult(r)">
  <h3 class="resultLink">
    <a href="${r['link']}">${boldTerm(r['product'])} - ${boldTerm(r['title'])}</a><br/>
  </h3>
  <p class="result">
    % if r['sentiment'] >= 0.7:
      <span class="good">Sentiment: ${int(r['sentiment'] * 100)}%</span><br/>
    % elif r['sentiment'] < 0.6:
      <span class="bad">Sentiment: ${int(r['sentiment'] * 100)}%</span><br/>
    % else:
      <span class="neutral">Sentiment: ${int(r['sentiment'] * 100)}%</span><br/>
    % endif
    ${boldTerm(summarize(r['content']))}
  </p>
</%def>

<%def name="tagCloud(good, bad)">
  <%
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
  %>
</%def>

## prints the data array for sentiment data; Note, this assumes that
## pointInterval is set to 10!
<%def name="sort(results)">
  <%
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
  %>
</%def>
