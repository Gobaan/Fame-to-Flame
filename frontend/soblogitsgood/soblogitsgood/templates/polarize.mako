<%inherit file="/sbig.mako" />
<%namespace name="helper" file="/helper.mako" />

<%def name="more_head_tags()">
  <script type="text/javascript" 
    src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">
  </script>
  <script type="text/javascript" src="scripts/sorting.js"></script>
  <script type="text/javascript">
    $.fn.exists = function() {
        return $(this).length !== 0;
    }

    timerid = 0

    function stopTimer()
    {
        clearInterval(timerid)
    }

    function loadResults()
    {
      $.ajax({async: false,
              url:  "getasyncresults",
              type: "POST",
              dataType: "xml",
              data: { query: "${c.query}" },
              success: function(data){
                $(data).find("stop").each(function(){
                    stopTimer();
                });
                $(data).find("result").each(function(){
                    source = $(this).find("source").text();
                    product = $(this).find("product").text();
                    cssprod = $(this).find("cssproduct").text();
                    sentiment = $(this).find("sentiment").text();

                    if(! $("#category" + source).exists()) {
                        $("#categories").append(
                            "<input checked=\"true\" type=\"checkbox\"" +
                            "id=\"category" + source + "\"><span class='sourcetitle'>" +
                            source + "<br>" +
                            "</span><ul class=\"categories\" id=\"cat" + source + "\">" +
                            "</ul>");
                        $("#category" + source).live("click", function() {
                            source = $(this).attr("id").substring(8);
                            if($(this).is(":checked")) {
                                $(".item" + source).show();
                                $("#cat" + source).slideDown();
                            } else {
                                $(".item" + source).hide();
                                $("#cat" + source).slideUp();
                            }
                        });
                    }

                    if(! $("#product" + cssprod).exists()) {
                        $("#cat" + source).append(
                            "<li>" +
                            "<input checked=\"true\" type=\"checkbox\"" +
                            "id=\"product" + cssprod + "\">" +
                            product +
                            "</li>");

                        $("#product" + cssprod).live("click", function() {
                            cssprod = $(this).attr("id").substring(7);
                            if($(this).is(":checked")) {
                                $(".prod" + cssprod).show();
                            } else {
                                $(".prod" + cssprod).hide();
                            }
                        });
                    }

                    if(sentiment < 0.6) {
                        $(".badresults").append(
                            "<div class=\"baditem\" sentiment=\"" + sentiment + "\">" +
                            "<div class=\"item" + source + "\">" +
                            "<div class=\"prod" + cssprod + "\">" +
                            $(this).find("content").text() +
                            "</div></div>");
                    } else if(sentiment >= 0.7) {
                        $(".goodresults").append(
                            "<div class=\"gooditem\" sentiment=\"" + sentiment + "\">" +
                            "<div class=\"item" + source + "\">" +
                            "<div class=\"prod" + cssprod + "\">" +
                            $(this).find("content").text() +
                            "</div></div></div>");
                    }
                });
              }
        });

      $('.gooditem').sortElements(function(a, b){
          return $(a).attr("sentiment") < $(b).attr("sentiment") ? 1 : -1;
      });
      $('.baditem').sortElements(function(a, b){
          return $(a).attr("sentiment") > $(b).attr("sentiment") ? 1 : -1;
      });
    }

    $(document).ready(function() {
      timerid = setInterval("loadResults()", 3000);
      loadResults();
      setTimeout("stopTimer()", 30000);
    });
  </script>
</%def>


<table class="polarize" align="center">
  ## Headers
  <tr>
    <td class="goodhead"></td>
    <td class="badhead"></td>
  </tr>
  ## Results
  <tr>
    <td class="goodresults">
    </td>
    <td class="badresults">
    </td>
  </tr>
</table>
