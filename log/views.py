from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import csv
from datetime import datetime
from decimal import Decimal
from io import StringIO

from .models import User, Contract, Transaction

# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "log/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "log/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "log/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "log/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "log/register.html")


def index(request):
    # Authenticated users view their trade
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user).order_by('-datetime').all()
        open_contracts = Contract.objects.filter(open_total__gt=0).order_by('-exp').all()
        if request.method == "POST":
            # There are 4 possible results for the request, each represented by a number from 4-7
            req = int(request.POST.get('first')) + int(request.POST.get('second'))
            results = index_helper(req)
        else:
            results = {}
        return render(request, "log/index.html", {
            "transactions": transactions,
            "results": results,
            "open_contracts": open_contracts
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


# figure out login_required
def upload(request):
    user = request.user
    last = Transaction.objects.filter(user=user).order_by('-datetime').first()
    if not last:
        last = "[SAMPLE] AMD $86 Call 08/07, 10 contracts averaging $1.49 ($1490)."
    if request.method == "POST":
        #try :
        counter = webull_uploader(request.POST['trades'], user)
        return render(request, "log/index.html", {
            "message": "Number of trades uploaded: " + str(counter)
        })
        #except Exception as e:
        #    print("***************")
        #    print("ERROR")
        #    print(f"'{str(e)}'")
        #    print("***************")
        #    return render(request, 'log/upload.html', {
        #        "last": last,
        #        "message": "Upload not successful.",
        #        "prefill": request.POST['trades']
        #    })
    return render(request, 'log/upload.html', {
        "last": last
    })

def webull_uploader(trades, user):
    # Turn textarea input into a csv "file" and read it in reverse order due to Webull putting latest trade first
    f = StringIO(trades)
    reader = csv.reader(f, delimiter=',')
    next(reader)
    counter = 0
    for row in reversed(list(reader)):
        # Skip cancelled and failed trade orders
        if row[3] != "Filled":
            continue
        # Skip repeat uploads, checking for exact same og_line, date, and avg
        avg = Decimal(row[7])
        date = datetime.strptime(row[10][:-4], '%m/%d/%Y %H:%M:%S')
        og_line = row[1]
        existent = Contract.objects.filter(og_line=og_line).first()
        if Transaction.objects.filter(og_line=existent).filter(datetime=date).filter(avg=avg).all():
            continue
        # Make quantity in a contract negative if "Sell" so it subtracts from an open position
        qty = int(row[4])
        side = row[2]
        if side == "Sell":
            qty = -qty
        # Create Contract object if doesn't exist yet
        exp = datetime.strptime(row[0].split()[1], '%m/%d/%Y').date()
        if not Contract.objects.filter(og_line=og_line).all():
            contract = Contract(
                user = user,
                og_line = og_line,
                exp = exp,
                avg = avg,
                open_qty = qty,
                open_total = avg * qty * 100
            )
            contract.save()
        # Update Contract object based on it being a sell or a buy
        else:
            c = Contract.objects.get(og_line=og_line)
            old_qty = c.open_qty
            old_total = c.open_total
            old_avg = c.avg
            if old_qty + qty == 0:
                c.avg = 0
                c.open_qty = 0
                c.open_total = 0
                c.save()
            elif row[2] == "Buy":
                c.avg = ((old_avg * old_qty) + (avg * qty)) / (old_qty + qty)
                c.open_qty = old_qty + qty
                c.open_total = ((((old_avg * old_qty) + (avg * qty)) / (old_qty + qty)) * (old_qty + qty)) * 100
                c.save()
            else:
                c.open_qty = old_qty + qty
                c.open_total = (old_avg * (old_qty + qty)) * 100
                c.save()
        # Invert sign for quantity to better represent totals in transactions
        qty = -qty
        # Create new Transaction
        transaction = Transaction(
            user = user,
            ticker = row[0].split()[0],
            exp = exp,
            opt = row[0].split()[4],
            strike = row[0].split()[5],
            side = row[2],
            qty = qty,
            avg = avg,
            total = qty * Decimal(row[7]) * 100,
            datetime = date,
            og_line = Contract.objects.get(og_line=og_line)
        )
        transaction.save()
        counter += 1
    return counter

def index_helper(req):
    results = {}
    total_trades = Transaction.objects.count()
    if req == 4:
        results['all'] = {'both': {}}
        results['all']['both']['ticker'] = "All Tickers"
        results['all']['both']['opt'] = "All Options"
        results['all']['both']['total'] = Transaction.objects.all().aggregate(Sum('total'))# - Contract.objects.filter(total__gt=0).all().aggregate(Sum('total'))
        results['all']['both']['trade_perc'] = f'100% ({total_trades} of {total_trades})'
    if req == 6:
        results['all'] = {'call': {}, 'put': {}}
        results['all']['call']['ticker'] = "All Tickers"
        results['all']['put']['ticker'] = "All Tickers"
        results['all']['call']['opt'] = "Calls"
        results['all']['put']['opt'] = "Puts"
        results['all']['call']['total'] = Transaction.objects.filter(opt="Call").all().aggregate(Sum('total'))
        results['all']['put']['total'] = Transaction.objects.filter(opt="Put").all().aggregate(Sum('total'))
        total_calls = Transaction.objects.filter(opt="Call").count()
        total_puts = Transaction.objects.filter(opt="Put").count()
        results['all']['call']['trade_perc'] = f'{round(total_calls / total_trades * 100)}% ({total_calls} of {total_trades})'
        results['all']['put']['trade_perc'] = f'{round(total_puts / total_trades * 100)}% ({total_puts} of {total_trades})'
    if req == 5:
        for ticker in Transaction.objects.values_list('ticker', flat=True).order_by('ticker').distinct():
            results[ticker] = {'both': {}}
            results[ticker]['both']['ticker'] = ticker
            results[ticker]['both']['opt'] = "All Options"
            results[ticker]['both']['total'] = Transaction.objects.filter(ticker=ticker).all().aggregate(Sum('total'))
            total_both = Transaction.objects.filter(ticker=ticker).count()
            results[ticker]['both']['trade_perc'] = f'{round(total_both / total_trades * 100)}% ({total_both} of {total_trades})'
    if req == 7:
        for ticker in Transaction.objects.values_list('ticker', flat=True).order_by('ticker').distinct():
            results[ticker] = {}
            if Transaction.objects.filter(ticker=ticker).filter(opt="Call").count():
                results[ticker]['call'] = {}
                results[ticker]['call']['ticker'] = ticker
                results[ticker]['call']['opt'] = "Calls"
                results[ticker]['call']['total'] = Transaction.objects.filter(ticker=ticker).filter(opt="Call").all().aggregate(Sum('total'))
                total_calls = Transaction.objects.filter(ticker=ticker).filter(opt="Call").count()
                results[ticker]['call']['trade_perc'] = f'{round(total_calls / total_trades * 100)}% ({total_calls} of {total_trades})'
            if Transaction.objects.filter(ticker=ticker).filter(opt="Put").count():
                results[ticker]['put'] = {}
                results[ticker]['put']['ticker'] = ticker
                results[ticker]['put']['opt'] = "Puts"
                results[ticker]['put']['total'] = Transaction.objects.filter(ticker=ticker).filter(opt="Put").all().aggregate(Sum('total'))
                total_puts = Transaction.objects.filter(ticker=ticker).filter(opt="Put").count()
                results[ticker]['put']['trade_perc'] = f'{round(total_puts / total_trades * 100)}% ({total_puts} of {total_trades})'
    return results


#   from log.models import User, Contract, Transaction
