document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#f1').addEventListener('submit', retrieve1);
    document.querySelector('#f2').addEventListener('submit', retrieve2);
    document.querySelector('#f3').addEventListener('submit', retrieve3);
    document.querySelector('#f4').addEventListener('submit', retrieve4);
    document.querySelector('#hs1').addEventListener('click', hide_show1);
    document.querySelector('#hs2').addEventListener('click', hide_show2);
    document.querySelector('#hs3').addEventListener('click', hide_show3);
    document.querySelector('#hs4').addEventListener('click', hide_show4);
});

function retrieve1() {
    event.preventDefault();
    document.querySelector('#tbody1').innerHTML = '';
    document.querySelector('#tbody1-2').innerHTML = '';
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
            document.querySelector('#tbody1').append(new_row);
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
            document.querySelector('#tbody1-2').prepend(new_row2);
        }
        var tables = document.querySelectorAll(".table1");
        tables.forEach(function(table) {
            table.style.display = 'table';
        });
        document.querySelector('#hs1').style.display = 'block';
    })
}

function retrieve2() {
    event.preventDefault();
    document.querySelector('#tbody2').innerHTML = '';
    document.querySelector('#tbody2-2').innerHTML = '';
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
            document.querySelector('#tbody2').append(new_row);
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
            document.querySelector('#tbody2-2').prepend(new_row2);
        }
        var tables = document.querySelectorAll(".table2");
        tables.forEach(function(table) {
            table.style.display = 'table';
        });
        document.querySelector('#hs2').style.display = 'block';
    })
}

function retrieve3() {
    event.preventDefault();
    document.querySelector('#tbody3').innerHTML = '';
    document.querySelector('#tbody3-2').innerHTML = '';
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
            document.querySelector('#tbody3').append(new_row);
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
            document.querySelector('#tbody3-2').prepend(new_row2);
        }
        var tables = document.querySelectorAll(".table3");
        tables.forEach(function(table) {
            table.style.display = 'table';
        });
        document.querySelector('#hs3').style.display = 'block';
    })
}

function retrieve4() {
    event.preventDefault();
    document.querySelector('#tbody4').innerHTML = '';
    document.querySelector('#tbody4-2').innerHTML = '';
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
            document.querySelector('#tbody4').append(new_row);
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
            document.querySelector('#tbody4-2').prepend(new_row2);
        }
        var tables = document.querySelectorAll(".table4");
        tables.forEach(function(table) {
            table.style.display = 'table';
        });
        document.querySelector('#hs4').style.display = 'block';
    })
}

function hide_show1() {
    console.log("Reached hideshow function");
    if (document.querySelector('#hs1').innerHTML === 'Show Daily Data') {
        console.log("Identifies inner html properly");
        document.querySelector('#hs1').innerHTML = 'Hide Daily Data';
        document.querySelector('#table1-2').style.display = 'table';
    } else {
        console.log("Doesn't identify inner html properly");
        document.querySelector('#hs1').innerHTML = 'Show Daily Data';
        document.querySelector('#table1-2').style.display = 'none';
    }
}

function hide_show2() {
    if (document.querySelector('#hs2').innerHTML === 'Show Daily Data') {
        document.querySelector('#hs2').innerHTML = 'Hide Daily Data';
        document.querySelector('#table2-2').style.display = 'table';
    } else {
        document.querySelector('#hs2').innerHTML = 'Show Daily Data';
        document.querySelector('#table2-2').style.display = 'none';
    }
}

function hide_show3() {
    if (document.querySelector('#hs3').innerHTML === 'Show Daily Data') {
        document.querySelector('#hs3').innerHTML = 'Hide Daily Data';
        document.querySelector('#table3-2').style.display = 'table';
    } else {
        document.querySelector('#hs3').innerHTML = 'Show Daily Data';
        document.querySelector('#table3-2').style.display = 'none';
    }
}

function hide_show4() {
    if (document.querySelector('#hs4').innerHTML === 'Show Daily Data') {
        document.querySelector('#hs4').innerHTML = 'Hide Daily Data';
        document.querySelector('#table4-2').style.display = 'table';
    } else {
        document.querySelector('#hs4').innerHTML = 'Show Daily Data';
        document.querySelector('#table4-2').style.display = 'none';
    }
}