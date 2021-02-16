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
// $(document).ready(function () {
//     $('#div_id_photo').addClass('custom-file')
//     $("label[for='id_photo']").addClass('custom-file-label')
//     $(".custom-file-input").change(function() {
//       var fileName = $(this).val().split("\\").pop();
//     $(this).siblings("label[for='id_photo']").addClass("selected").html(fileName);
//     $("label[for='id_photo']").addClass('custom-file-label').html(fileName)
//     });
// })