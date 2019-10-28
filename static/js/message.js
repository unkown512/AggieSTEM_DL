$(document).ready(function() {
  $("#txtmsg").on('click', function() {
    $("#emailmsg").prop("checked", false);
  });
  $("#emailmsg").on('click', function() {
    $("#txtmsg").prop("checked", false);
  });
});
