document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#refresh-expired').addEventListener('click', refresh_expired);
})

function refresh_expired() {
    fetch('', {
        method: 'PUT'
    })
    .then(location.reload())
}
