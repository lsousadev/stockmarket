document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#f1').addEventListener('submit', retrieve1);
    document.querySelector('#f2').addEventListener('submit', retrieve2);
    document.querySelector('#f3').addEventListener('submit', retrieve3);
    document.querySelector('#f4').addEventListener('submit', retrieve4);
});

function retrieve1() {
    event.preventDefault();
    document.querySelector('#tbody1').innerHTML = '';
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            ticker: document.querySelector('#t1').value,
            start: document.querySelector('#ds1').value,
            end: document.querySelector('#de1').value
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
            document.querySelector('#tbody1').append(new_row);
        }
    })
}

function retrieve2() {
    event.preventDefault();
    document.querySelector('#tbody2').innerHTML = '';
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            ticker: document.querySelector('#t2').value,
            start: document.querySelector('#ds2').value,
            end: document.querySelector('#de2').value
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
            document.querySelector('#tbody2').append(new_row);
        }
    })
}

function retrieve3() {
    event.preventDefault();
    document.querySelector('#tbody3').innerHTML = '';
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            ticker: document.querySelector('#t3').value,
            start: document.querySelector('#ds3').value,
            end: document.querySelector('#de3').value
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
            document.querySelector('#tbody3').append(new_row);
        }
    })
}

function retrieve4() {
    event.preventDefault();
    document.querySelector('#tbody4').innerHTML = '';
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            ticker: document.querySelector('#t4').value,
            start: document.querySelector('#ds4').value,
            end: document.querySelector('#de4').value
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
            document.querySelector('#tbody4').append(new_row);
        }
    })
}