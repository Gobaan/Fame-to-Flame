<%inherit file="/sbig.mako" />

<%def name="more_head_tags()">
<script type="text/javascript" 
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js">
</script>

<script type="text/javascript">

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

$(document).ready(function() {
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
        $("#cat" + source).show();
    } else {
        $("#cat" + source).hide();
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
</script>
</%def>

<br/>
<br/>
<center>
Sorry, your search <b>${c.query}</b> had no results.
</center>
