<%inherit file="/sbig.mako" />
<%namespace name="helper" file="/helper.mako" />

<%def name="more_head_tags()">
  <script type="text/javascript"
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>

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
                    if(! $("#results" + source).exists()) {
                        $("#allresults").append("<div id=\"results" + source +
                            "\"><h2>" + source + "</h2></div>\n");
                        $("#categories").append(
                            "<input checked=\"true\" type=\"checkbox\"" +
                            "id=\"category" + source + "\">" +
                            source +
                            "<ul class=\"categories\" id=\"cat" + source + "\">" +
                            "</ul>");
                        $("#category" + source).live("click", function() {
                            source = $(this).attr("id").substring(8);
                            if($(this).is(":checked")) {
                                $("#results" + source).show();
                                $("#cat" + source + " input").attr("checked", "true");
                            } else {
                                $("#results" + source).hide();
                                $("#cat" + source + " input").attr("checked", "false");
                            }
                        });
                    }
                    prod = $(this).find("cssproduct").text();

                    if(! $("#prod" + prod).exists()) {
                        $("#cat" + source).append(
                            "<li id=\"prod" + prod + "\">" +
                            "<input checked=\"true\" type=\"checkbox\"" +
                            "id=\"product" + prod + "\">" +
                            product +
                            "</li>");

                        $("#product" + prod).live("click", function() {
                            prod = $(this).attr("id").substring(7);
                            if($(this).is(":checked")) {
                                $(".prod" + prod).show();
                            } else {
                                $(".prod" + prod).hide();
                            }
                        });
                    }

                    $("#results" + source).append("<div class=\"prod" + prod + "\">" +
                            $(this).find("content").text() + "</div>");
                });
              }
        });
    }

    $(document).ready(function() {
      timerid = setInterval("loadResults()", 3000);
      loadResults();
      setTimeout("stopTimer()", 30000);
    });
  </script>
</%def>

<div id="allresults">
</div>
