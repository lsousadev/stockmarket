document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach((form) => {
        form.addEventListener('submit', retrieve);
    });

    const hideShow = document.querySelectorAll('.hide-show');
    hideShow.forEach((button) => {
        button.addEventListener('click', hide_show);
    });
});

function retrieve() {
    event.preventDefault();
    const baseForm = event.target.parentNode;
    const mainForm = baseForm.querySelector('tbody.first');
    const secondaryForm =  baseForm.querySelector('tbody.second')
    mainForm.innerHTML = '';
    secondaryForm.innerHTML = '';
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
        for (var i = 0; i < 5; i++) {
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

            mainForm.append(new_row);
        }
        for (var i = 0; i < data[5].length; i++) {
            const new_row2 = document.createElement('tr');
            const date2 = document.createElement('td');
            date2.innerHTML = `${data[5][i].date}`;
            const weekday2 = document.createElement('td');
            weekday2.innerHTML = `${data[5][i].weekday}`;
            const open2 = document.createElement('td');
            open2.innerHTML = `$${data[5][i].open}`;
            const close2 = document.createElement('td');
            close2.innerHTML = `$${data[5][i].close}`;
            const overnight2 = document.createElement('td');
            overnight2.innerHTML = `${data[5][i].overnight}%`;
            const intraday2 = document.createElement('td');
            intraday2.innerHTML = `${data[5][i].intraday}%`;
            const sum_onid2 = document.createElement('td');
            sum_onid2.innerHTML = `${data[5][i].overall}%`;
            new_row2.append(date2);
            new_row2.append(weekday2);
            new_row2.append(open2);
            new_row2.append(close2);
            new_row2.append(overnight2);
            new_row2.append(intraday2);
            new_row2.append(sum_onid2);

            secondaryForm.prepend(new_row2);
        }
        var tables = baseForm.querySelectorAll("table.first");
        tables.forEach(function(table) {
            table.style.display = 'table';
        });
        baseForm.querySelector('.hide-show').style.display = 'block';
    })
}



function hide_show() {
    const baseForm = event.target.parentNode;
    if (baseForm.querySelector('.hide-show').innerHTML === 'Show Daily Data') {
        baseForm.querySelector('.hide-show').innerHTML = 'Hide Daily Data';
        baseForm.querySelector('table.second').style.display = 'table';
    } else {
        baseForm.querySelector('.hide-show').innerHTML = 'Show Daily Data';
        baseForm.querySelector('table.second').style.display = 'none';
    }
}