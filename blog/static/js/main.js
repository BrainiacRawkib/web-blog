/* alert message timeout */
setTimeout(function () {
    $('#alert-message').fadeOut('slow');
}, 3000)

/* spinner wrapper */
let spinnerWrapper = document.querySelector('.spinner-wrapper');
window.addEventListener('load', function () {
    spinnerWrapper.parentElement.removeChild(spinnerWrapper);
});

/* custom file upload */
$(".form-control-file").on("change", function() {
  let fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});