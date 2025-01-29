 // Show menu links on burger click
 $("#menu-btn").click(function () {
    $("nav .navigation ul").addClass("active");
  });

  // Hide navbar on click function
  $("#menu-close").click(function () {
    $("nav .navigation ul").removeClass("active");
  });