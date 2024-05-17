//use Jquery Object
$(document).ready(function () {
  // change the background color of the nav-item when mouse hover
  $(".nav-item").on("mouseenter", function () {
    $(this).css({
      "border-radius": "10px",
      "background-color": "rgb(229, 231, 235, 0.5)",
    });
  });

  $(".nav-item").on("mouseleave", function () {
    $(this).css({
      "border-radius": "",
      "background-color": "",
      "box-shadow": "",
    });
  });

  // Easter egg, do not click the image
  $(".click_icon")
    .click(function () {
      alert("Baited! This is a picture, not a link. XD");
    })
    .css("cursor", "pointer");

  // create hyperlink
  function createLink() {
    var url = document.getElementById("linkInput").value;
    var displayLink = document.getElementById("linkHere");
    displayLink.innerHTML = '<a href="' + url + '">' + "Visit " + url + "</a>";
    displayLink.firstChild.target = "_blank";
  }

  // Ajax request to Wikipedia API
  var timeoutId;
  $("#searchBox").on("input", function () {
    clearTimeout(timeoutId);
    var query = $(this).val();
    if (query !== "") {
      timeoutId = setTimeout(function () {
        $.ajax({
          url:
            "https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search=" +
            query,
          dataType: "jsonp",
          success: function (data) {
            var suggestionList = $("#suggestionList");
            suggestionList.empty();
            data[1].forEach(function (item) {
              $("<li>")
                .addClass("list-group-item list-group-item-action")
                .text(item)
                .appendTo(suggestionList)
                .on("click", function () {
                  $("#searchBox").val($(this).text());
                  suggestionList.empty();
                });
            });
          },
        });
      }, 300);
    } else {
      $("#suggestionList").empty();
    }
  });

  $("#searchButton").on("click", function () {
    var query = $("#searchBox").val();
    window.open("https://en.wikipedia.org/wiki/" + query, "_blank");
  });

  $(document).on("click", function (e) {
    if (!$(e.target).closest("#searchBox").length) {
      $("#suggestionList").empty();
    }
  });

  $("#searchBox").keydown(function (e) {
    if (e.keyCode === 13) {
      e.preventDefault();
      $("#suggestionList li").first().trigger("click");
    }
  });
});
