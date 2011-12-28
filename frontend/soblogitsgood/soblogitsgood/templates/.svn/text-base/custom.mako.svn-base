<%inherit file="/sbig.mako" />
<%namespace name="helper" file="/helper.mako" />

<%def name="more_head_tags()">
  <link rel="stylesheet" type="text/css" href="styles/custom-theme/jquery-ui-1.8.10.custom.css" />

  <script type="text/javascript"
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>
  <script type="text/javascript" src="scripts/jquery-ui-1.8.2.custom.min.js"></script>

  <script type="text/javascript">
  $(document).ready(function() {
    $(".slider").slider({
        range: true,
        min: 0,
        max: 1,
        step: 0.1,
        values: [0, 1],
        slide: function(event, ui) {
            $(".slider-display").html("Viewing "
                + ui.values[0]*100 + "% to " + ui.values[1]*100 + "%");
            $(".item").each(function(){
                sent = $(this).attr("sentiment");
                bot = ui.values[0];
                top = ui.values[1];
                if(sent >= bot && sent <= top) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        }
    });
  });
</script>

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

                $("#allresults").append(
                        "<div class=\"item\" sentiment=\"" + sentiment + "\">" +
                        "<div class=\"item" + source + "\">" +
                        "<div class=\"prod" + cssprod + "\">" +
                        $(this).find("content").text() +
                        "</div></div>");
            });

            $(".item").each(function(){
                sent = $(this).attr("sentiment");
                bot = $(".slider").slider("values")[0];
                top = $(".slider").slider("values")[1];
                if(sent >= bot && sent <= top) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
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

<div width="100%" align="center">
##  Viewing ${int(c.start*100)}% to ${int(c.end*100)}%
  <div class="slider"></div>
  <span class="slider-display">
    Viewing 0% to 100%
  </span>
  <br />
</div>
<br/>

<div id="allresults"></div>
