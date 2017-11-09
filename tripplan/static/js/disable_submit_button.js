$(document).ready(setup);
function setup() {
  $('form').submit(function() {
    $(".click-disable").prop('disabled',true);
  });
}
