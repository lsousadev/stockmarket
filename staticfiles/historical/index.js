document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    for (var i = 0; i < forms.length; i++) {
        forms.addEventListener('submit', retrieve);
    }
});

function retrieve() {
    event.preventDefault();
    const baseForm = event.target.parentNode;
    baseForm.querySelector('tbody'.innerHTML) = '';
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            ticker: baseForm.querySelector('.ticker').value,
            start: baseForm.querySelector('.start-date').value,
            end: baseForm.querySelector('.end-date').value
        })
    })
    .then(response => response.json())
    .then(data => {
        for (var i = 0; i < data.length; i++) {
            const new_row = document.createElement('tr');
            const weekday = document.createElement('td');
            weekday.innerHTML = `<strong>${data[i].weekday}</strong>`;
            const overnight = document.createElement('td');
            overnight.innerHTML = `${data[i].overnight}%`;
            const intraday = document.createElement('td');
            intraday.innerHTML = `${data[i].intraday}%`;
            const sum_onid = document.createElement('td');
            sum_onid.innerHTML = `${data[i].sum_onid}%`;
            const positive_overnights = document.createElement('td');
            positive_overnights.innerHTML = `${data[i].positive_overnights}%`;
            const positive_intradays = document.createElement('td');
            positive_intradays.innerHTML = `${data[i].positive_intradays}%`;
            const positive_sum_onids = document.createElement('td');
            positive_sum_onids.innerHTML = `${data[i].positive_sum_onids}%`;
            const total_days = document.createElement('td');
            total_days.innerHTML = `${data[i].total_days}`;
      
            new_row.append(weekday);
            new_row.append(overnight);
            new_row.append(intraday);
            new_row.append(sum_onid);
            new_row.append(positive_overnights);
            new_row.append(positive_intradays);
            new_row.append(positive_sum_onids);
            new_row.append(total_days);
            baseForm.querySelector('tbody').append(new_row);
        }
    });
}