$(document).ready(function() {
  // Handler when expand sidebar button is clicked
  $('[data-toggle=offcanvas]').on('click', function() {
    // open sidebar
    $('#sidebar').addClass('display-menu');
    $('#dismiss').addClass('display-menu');
    // fade in the overlay
    $('.overlay').fadeIn();
  });

  // Handler when dismiss or overlay is clicked
  $('#dismiss, .overlay').on('click', function() {
    //hide the sidebar
    $('#sidebar').removeClass('display-menu');
    $('#dismiss').removeClass('display-menu');
    // fade out the overlay
    $('.overlay').fadeOut();
  });

});
