document.addEventListener('DOMContentLoaded', function() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;

    document.querySelector('#refresh-expired').addEventListener('click', refresh_expired);
    document.querySelector('#date-end').value = today;
})

function refresh_expired() {
    fetch('', {
        method: 'PUT'
    })
    .then(location.reload())
}
