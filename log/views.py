from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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


@login_required(login_url='/log/login')
@csrf_exempt
def index(request):
    open_contracts = Contract.objects.filter(user=request.user).filter(open_qty__gt=0).order_by('-exp').all()
    if request.method == "PUT":
        expired = open_contracts.filter(exp__lt=datetime.now().date()).all()
        for contract in expired:
            contract.open_avg = 0
            contract.open_qty = 0
            contract.open_total = 0
            contract.save()
        open_contracts = Contract.objects.filter(user=request.user).filter(open_qty__gt=0).order_by('-exp').all()
        return JsonResponse({'success': True})
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp').all()
    if request.method == "POST":
        # There are 4 possible results for the request, each represented by a number from 4-7
        req = int(request.POST.get('first')) + int(request.POST.get('second'))
        user = request.user
        results = index_helper(req, user)
    else:
        results = {}
    return render(request, "log/index.html", {
        "open_contracts": open_contracts,
        "results": results,
        "transactions": transactions
    })


# Figure out login_required
@login_required(login_url='/log/login')
def upload(request):
    user = request.user
    last = Transaction.objects.filter(user=user).order_by('-timestamp').first()
    if not last:
        last = "No transactions uploaded."
    if request.method == "POST":
        #try :
        counter = webull_uploader(request.POST['trades'], user)
        return render(request, "log/upload.html", {
            "message": f"Number of trades uploaded: {counter}."
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
    print(reader)
    # If first line is header, skip
    next(reader)
    counter = 0
    for row in reversed(list(reader)):
        # Skip cancelled and failed trade orders
        if row[3] != "Filled":
            continue
        # Unpack all data
        user = user     # May not be necessary
        ticker = row[0].split()[0]
        exp = datetime.strptime(row[0].split()[1], '%m/%d/%Y').date()
        opt = row[0].split()[4]
        strike = row[0].split()[5]
        side = row[2]
        qty = int(row[4])
        avg = Decimal(row[7])
        timestamp = datetime.strptime(row[10][:-4], '%m/%d/%Y %H:%M:%S')
        ref = row[1]      # Could be row[0] as well
        # Skip repeat uploads, checking for exact same date and avg. Might need to add contract to filters
        if Transaction.objects.filter(timestamp=timestamp).filter(avg=avg).all():
            continue
        # Create Contract object if doesn't exist yet
        if not Contract.objects.filter(ref=ref).all():
            contract = Contract(
                user = user,
                ticker = ticker,
                exp = exp,
                opt = opt,
                strike = strike,
                open_avg = avg,
                open_qty = qty,
                open_total = avg * qty * 100,
                ref = ref
            )
            contract.save()
        # Update Contract object based on it being a sell or a buy
        else:
            c = Contract.objects.get(ref=ref)
            old_avg = c.open_avg
            old_qty = c.open_qty
            old_total = c.open_total
            # Make sell qty negative for Contract purposes
            if side == "Sell":
                qty = -qty
            # If closing position, set all to 0
            if old_qty + qty == 0:
                c.open_avg = 0
                c.open_qty = 0
                c.open_total = 0
                c.save()
            elif row[2] == "Buy":
                c.open_avg = ((old_avg * old_qty) + (avg * qty)) / (old_qty + qty)
                c.open_qty = old_qty + qty
                c.open_total = ((((old_avg * old_qty) + (avg * qty)) / (old_qty + qty)) * (old_qty + qty)) * 100
                c.save()
            else:
                c.open_qty = old_qty + qty
                c.open_total = old_avg * (old_qty + qty) * 100
                c.save()
        # Switch qty signals for transactions
        qty = -qty
        # Create new Transaction
        transaction = Transaction(
            user = user,
            contract = Contract.objects.get(ref=ref),
            side = side,
            qty = qty,
            avg = avg,
            total = qty * avg * 100,
            timestamp = timestamp
        )
        transaction.save()
        counter += 1
    return counter

def index_helper(req, user):
    results = {}
    user_contracts = Contract.objects.filter(user=user).all()
    user_transactions = Transaction.objects.filter(user=user).all()
    total_trades = user_transactions.count()
    if req == 4:
        results['all'] = {'both': {}}
        results['all']['both']['ticker'] = "All Tickers"
        results['all']['both']['opt'] = "All Options"
        results['all']['both']['total'] = user_transactions.aggregate(Sum('total'))['total__sum']
        results['all']['both']['trade_perc'] = f'100% ({total_trades} of {total_trades})'
    if req == 6:
        results['all'] = {'call': {}, 'put': {}}
        results['all']['call']['ticker'] = "All Tickers"
        results['all']['put']['ticker'] = "All Tickers"
        results['all']['call']['opt'] = "Calls"
        results['all']['put']['opt'] = "Puts"
        results['all']['call']['total'] = user_transactions.filter(contract__opt="Call").aggregate(Sum('total'))['total__sum']
        results['all']['put']['total'] = user_transactions.filter(contract__opt="Put").aggregate(Sum('total'))['total__sum']
        total_calls = user_transactions.filter(contract__opt="Call").count()
        total_puts = user_transactions.filter(contract__opt="Put").count()
        results['all']['call']['trade_perc'] = f'{round(total_calls / total_trades * 100)}% ({total_calls} of {total_trades})'
        results['all']['put']['trade_perc'] = f'{round(total_puts / total_trades * 100)}% ({total_puts} of {total_trades})'
    if req == 5:
        for ticker in user_contracts.values_list('ticker', flat=True).order_by('ticker').distinct(): # check end of page for possible ordering by transactions
            results[ticker] = {'both': {}}
            results[ticker]['both']['ticker'] = ticker
            results[ticker]['both']['opt'] = "All Options"
            results[ticker]['both']['total'] = user_transactions.filter(contract__ticker=ticker).aggregate(Sum('total'))['total__sum']
            total_both = user_transactions.filter(contract__ticker=ticker).count()
            results[ticker]['both']['trade_perc'] = f'{round(total_both / total_trades * 100)}% ({total_both} of {total_trades})'
    if req == 7:
        for ticker in user_contracts.values_list('ticker', flat=True).order_by('ticker').distinct(): # check end of page for possible ordering by transactions
            results[ticker] = {}
            if user_transactions.filter(contract__ticker=ticker).filter(contract__opt="Call").count():
                results[ticker]['call'] = {}
                results[ticker]['call']['ticker'] = ticker
                results[ticker]['call']['opt'] = "Calls"
                results[ticker]['call']['total'] = user_transactions.filter(contract__ticker=ticker).filter(contract__opt="Call").aggregate(Sum('total'))['total__sum']
                total_calls = user_transactions.filter(contract__ticker=ticker).filter(contract__opt="Call").count()
                results[ticker]['call']['trade_perc'] = f'{round(total_calls / total_trades * 100)}% ({total_calls} of {total_trades})'
            if user_transactions.filter(contract__ticker=ticker).filter(contract__opt="Put").count():
                results[ticker]['put'] = {}
                results[ticker]['put']['ticker'] = ticker
                results[ticker]['put']['opt'] = "Puts"
                results[ticker]['put']['total'] = user_transactions.filter(contract__ticker=ticker).filter(contract__opt="Put").aggregate(Sum('total'))['total__sum']
                total_puts = user_transactions.filter(contract__ticker=ticker).filter(contract__opt="Put").count()
                results[ticker]['put']['trade_perc'] = f'{round(total_puts / total_trades * 100)}% ({total_puts} of {total_trades})'
    return results


#   from log.models import User, Contract, Transaction

# The proper way to do this is with annotation.
# This will reduce the amount of database queries to 1, and ordering will be a simple order_by function:
# from django.db.models import Count
# cat_list = Category.objects.annotate(count=Count('project_set__id')).order_by('count')