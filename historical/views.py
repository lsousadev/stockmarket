import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from datetime import date, datetime
import yfinance

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "POST":
        # Get parameters of request
        data = json.loads(request.body)
        ticker = data['ticker']
        start_date = data['start']
        end_date = data['end']
        # yfinance API
        data = yfinance.Ticker(ticker)
        hist = data.history(start=start_date, end=end_date)
        total_days_received = len(hist.index)
        # Set first overnight to 0 by matching non-existing close to first open
        lastclose = hist.at[hist.index[0], 'Open']
        # Translator for .weekday()
        response_data = [{"weekday": "Monday"}, {"weekday": "Tuesday"}, {"weekday": "Wednesday"}, {"weekday": "Thursday"}, {"weekday": "Friday"}]
        # Start counters for positive overnights, intradays, and days for % stats
        for day in response_data:
            day['overnight'] = 0
            day['intraday'] = 0
            day['sum_onid'] = 0
            day['positive_overnights'] = 0
            day['positive_intradays'] = 0
            day['positive_sum_onids'] = 0
            day['total_days'] = 0
            day['volume'] = 0
        # Loop for data and populate response
        for line in hist.index:
            weekday = datetime.strptime(str(line)[:-9], '%Y-%m-%d').date().weekday()
            open_price = hist.at[line, 'Open']
            close_price = hist.at[line, 'Close']
            # print(f"Weekday: {weekday} | Priceopen: {priceopen} | Priceclose: {priceclose} | Lastclose: {lastclose}")
            response_data[weekday]['overnight'] += (open_price - lastclose) / lastclose
            response_data[weekday]['intraday'] += (close_price - open_price) / open_price
            response_data[weekday]['sum_onid'] += (close_price - lastclose) / lastclose
            if (open_price - lastclose) / lastclose >= 0:
                response_data[weekday]['positive_overnights'] += 1
            if (close_price - open_price) / open_price >= 0:
                response_data[weekday]['positive_intradays'] += 1
            if (close_price - lastclose) / lastclose >= 0:
                response_data[weekday]['positive_sum_onids'] += 1
            response_data[weekday]['total_days'] += 1
            response_data[weekday]['volume'] += hist.at[line, 'Volume']
            lastclose = close_price
        # Prepare response_data to be sent while making sure all days from data were utilized
        final_check = 0
        for day in response_data:
            total_days = day['total_days']
            final_check += total_days
            day['overnight'] = round((day['overnight'] / total_days) * 100, 2)
            day['intraday'] = round((day['intraday'] / total_days) * 100, 2)
            day['sum_onid'] = round((day['sum_onid'] / total_days) * 100, 2)
            day['positive_overnights'] = round((day['positive_overnights'] / total_days) * 100)
            day['positive_intradays'] = round((day['positive_intradays'] / total_days) * 100)
            day['positive_sum_onids'] = round((day['positive_sum_onids'] / total_days) * 100)
            day['volume'] = round((day['volume'] / total_days) / 1000000)
        if final_check != total_days_received:
            return JsonResponse({
                "error": "Something went wrong. Days requested: {total_days_received} | Days processed: {final_check}"
            }, status=400)
        return JsonResponse(response_data, status=200, safe=False)
    # If response.method == "GET":
    return render(request, "historical/index.html")