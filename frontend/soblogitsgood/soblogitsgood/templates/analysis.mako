<%inherit file="/sbig.mako" />
<%namespace name="helper" file="/helper.mako" />

<%def name="more_head_tags()">
  <script type="text/javascript" 
    src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">
  </script>
  <script type="text/javascript" src="scripts/highcharts.js"></script>

<script type="text/javascript">
var piechart;
$(document).ready(function() {
  piechart = new Highcharts.Chart({
    chart: {
      renderTo: 'pie',
      margin: [0,0,0,0]
    },
    title: {
      text: null,
    },
    tooltip: {
      formatter: function() {
        return '<b>'+ this.point.name +'</b>: '+ this.y +' results';
      }
    },
    plotOptions: {
      pie: {
        borderColor: '#FFFFFF',
        borderWidth: 3,
        cursor: 'pointer',
        dataLabels: {
            distance: -35,
            enabled: false,
            formatter: function() {
              if (this.percentage > 10) return this.point.name;
            },
            style: {
              font: '13px Trebuchet MS, Verdana, sans-serif',
            }
        }
      }
    },
    legend: {
      enabled: false,
      layout: 'vertical',
      style: {
        left: 'auto',
        bottom: 'auto',
        right: '0px',
        top: '0px'
      }
    },
    series: [{
      type: 'pie',
      name: 'Good vs. Bad',
      data: [
        {
          name: 'Good',  
          y: ${len(c.goodResults)},
          color: '#49BD43'
        },
        {
          name: 'Mediocre',  
          y: ${len(c.neutralResults)},
          color: '#a1884b'
        },
        {
          name: 'Bad',
          y: ${len(c.badResults)},
          color: '#F95353'
        },
      ]
    }]
  });
});

var linechart;
$(document).ready(function() {
    linechart = new Highcharts.Chart({
        chart: {
            renderTo: 'line',
            defaultSeriesType: 'line',
            marginRight: 30,
            marginBottom: 75
        },
        title: {
            text: null,
            style: {
                color: '#F95353',
            },
            x: -20 //center
        },
        yAxis: {
            gridLineColor: '#FED9D8',
            allowDecimals: false,
            min: 0,
            title: {
                text: 'Number of Reviews',
                style: {
                    color: '#49BD43',
                }
            },
            labels: {
                style: {
                    color: '#F95353',
                }
            }
        },
        xAxis: {
            tickColor: '#FCA2A2',
            lineColor: '#FCA2A2',
            title: {
                text: 'Sentiment Score',
                style: {
                    color: '#49BD43',
                }
            },
            plotLines: [{
                dashStyle: 'dash',
                value: ${c.mean*100},
                width: 1.5,
                color: '#FCA2A2',
                zIndex: 5,
                label: {
                    style: {
                        color: '#F95353',
                        fontWeight: 'bold',
                    },
                    text: 'Average: '+ Math.round(${c.mean}*100)+ '%',
                }
            }],
            labels: {
                formatter: function() {
                    return this.value + '%';
                },
                style: {
                    color: '#F95353',
                }
            }
        },
        tooltip: {
            formatter: function() {
                return this.x +'%: '+ this.y + ' reviews';
            }
        },
        legend: {
            enabled: false,
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -10,
            y: 100,
            borderWidth: 0
        },
        series: [
            {name: 'Results', color: '#363636', pointInterval: 10, data:
                    ${helper.sort(c.results)}},
        ]
        
    });
});
    
$(document).ready(function(){
  //$("#stats_body").hide();
  
  $("#overview_header").toggle(function(){
    $("#overview_graphs").slideDown();
    $("#overview_header").html("Overview [-]")
  }, function() {
    $("#overview_graphs").slideUp();
    $("#overview_header").html("Overview [+]")
  });

  $("#stats_header").toggle(function(){
    $("#stats_body").slideDown();
    $("#stats_header").html("Statistics [-]")
  }, function() {
    $("#stats_body").slideUp();
    $("#stats_header").html("Statistics [+]")
  });

  $("#narrow").bind("click", function(){
    params = new Array();
    params["query"] = "${c.query}";
    params["narrow"] = true;
    // Build restrictions
    products = new Array();
    sources = new Array();

    $(".sourcecheck").each(function() {
        if($(this).is(":checked")) {
            sources.push($(this).attr("id"));
        }
    });

    $(".prodcheck").each(function() {
        if($(this).is(":checked")) {
            products.push($(this).attr("id"));
        }
    });

    params["products"] = products;
    params["sources"] = sources;
    post_to_url("analysis", params)
  });

  $(".sourcecheck").live("click", function() {
    source = $(this).attr("id").substring(8);
    if($(this).is(":checked")) {
        $("#cat" + source).slideDown();
    } else {
        $("#cat" + source).slideUp();
    }
  });

  $(".sourcecheck").each(function() {
    source = $(this).attr("id").substring(8);
    if($(this).is(":checked")) {
        $("#cat" + source).show();
    } else {
        $("#cat" + source).hide();
    }
  });
});

function post_to_url(path, params) {
    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", path);

    for(var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", params[key]);

        form.appendChild(hiddenField);
    }

    document.body.appendChild(form);    // Not entirely sure if this is necessary
    form.submit();
}

</script>
</%def>

<table width="100%" cellspacing="0">
<tr>
  <td class="leftcorner" style="background-image:
      url('../images/goodcorner.png');">
      <p />
  </td>
  <td id="overview_header" class="graphheader">
    Overview [-]
  </td>
  <td class="rightcorner" style="background-image: 
      url('../images/rgoodcorner.png');">
      <p />
  </td>
</tr>
<tr>
  <td colspan="3">
    <div id="overview_graphs">
      <table>
        <tr>
          <td>
            <div id="pie" style="width: 300px; height: 250px; margin: 0 auto"></div>
          </td>
          <td class="tagcloud">
            ${helper.tagCloud(c.goodTerms, c.badTerms)}
          </td>
        </tr>
      </table>
    </div>
  </td>
</tr>
<tr>
  <td class="leftcorner" style="background-image:
      url('../images/goodcorner.png');">
      <p />
  </td>
  <td id="stats_header" class="graphheader">
    Statistics [-]
  </td>
  <td class="rightcorner" style="background-image: 
      url('../images/rgoodcorner.png');">
      <p />
  </td>
</tr>
<tr>
  <td colspan="3">
  <div id="stats_body">
      <p align="center">
      Verdict: ${c.verdict}
      </p>
      <div id="stats_graphs">
        <div id="line" style="width: 700px; height: 400px; margin: 0 auto"></div>
      </div>
  </div>
  </td>
</tr>
</table>

##set vi: sw=4 ts=4 sts=4:
