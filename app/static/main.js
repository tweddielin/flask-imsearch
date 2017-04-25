// ----- custom js ----- //
// global
var url = 'INRIA/jpg/';
var data = [];
// hide initial
$("#searching").hide();
$("#results-table").hide();
$("#error").hide();

$(function() {

  // sanity check
  console.log( "ready!" );

  // image click
  $(".img").click(function() {

    // empty/hide results
    $("#results").empty();
    $("#results-table").hide();
    $("#error").hide();

    // remove active class
    $(".img").removeClass("active")

    // add active class to clicked picture
    $(this).addClass("active")

    // grab image url
    var image = $(this).attr("src")
    console.log(image)

    // show searching text
    $("#searching").show();
    console.log("searching...")

    // show table
    $("#results-table").show();

    // ajax request
    $.ajax({
      type: "POST",
      url: "/search",
      data : { img : image },
      // handle success
      success: function(result) {
        console.log(result.results);
        var data = result.results
        // show table
        $("#results-table").show();
        $("#searching").hide();
        // loop through results, append to dom
        for (i = 0; i < data.length; i++) {
            $("#results").append('<tr><th><a href="'+url+data[i]["image"]+'" target="_blank"'+'"><img src="'+url+data[i]["image"]+
            '" class="result-img"></a></th><th>'+data[i]['score']+'</th></tr>')

        };
      },
      // handle error
      error: function(error) {
        console.log(error);

        // show error
        $("#error").append();
      }
    });

  });

});
