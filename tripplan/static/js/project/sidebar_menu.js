$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('#sidebar').toggleClass('display-menu');
    $('#content').toggleClass('display-menu');
    $('#navbar-toggle').find('i').toggleClass('fa-angle-double-right fa-angle-double-left');
  });
});
