<%inherit file="/sbig.mako" />

<%def name="more_head_tags()">
  <script type="text/javascript"
  src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js"></script>

  <script type="text/javascript">
    $(document).ready(function() {
      $("#testing").append("abcd");

      $.ajax({async: false,
              url:  "testajax",
              type: "POST",
              dataType: "xml",
              success: function(data){
                    $(data).find("result").each(function(){
                        $("#testing").append($(this).find("source").text());
                    });
              }
        });
    });
  </script>
</%def>

<div id="testing">
</div>
