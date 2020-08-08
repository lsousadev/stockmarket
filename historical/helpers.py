from django.db.models import Avg, Count
import yfinance
from historical.models import Ticker, Historical

def yf(stock, model):
    # yfinance API
    data = yfinance.Ticker(stock)
    hist = data.history(period="1y")
    # Set first overnight to 0 by matching non-existing close to first open
    lastclose = hist.at[hist.index[0], 'Open']
    # Translator for .weekday()
    days_of_week = {
        0: "MON",
        1: "TUE",
        2: "WED",
        3: "THU",
        4: "FRI"
    }
    # loop for data
    for date in hist.index:
        weekday = days_of_week[date.weekday()]
        date = str(date)[:-9]
        priceopen = hist.at[date, 'Open']
        priceclose = hist.at[date, 'Close']
        # print(f"Date: {date} | Priceopen: {priceopen} | Priceclose: {priceclose} | Lastclose: {lastclose}")
        overnight = round(((priceopen - lastclose) / lastclose) * 100, 2)
        intraday = round(((priceclose - priceopen) / priceopen) * 100, 2)
        sum24 = round(((priceclose - lastclose) / lastclose) * 100, 2)
        # print(f"Overnight: {overnight} (type: {type(overnight)}) | Intraday: {intraday} (type: {type(intraday)}) | Sum24: {sum24} (type: {type(sum24)})")
        volume = hist.at[date, 'Volume']
        high = hist.at[date, 'High']
        low = hist.at[date, 'Low']
        lastclose = priceclose
        h = Historical(
            ticker = model,
            date = date,
            weekday = weekday,
            priceopen = priceopen,
            priceclose = priceclose,
            overnight = overnight,
            intraday = intraday,
            sum24 = sum24,
            volume = volume,
            high = high,
            low = low
        )
        h.save()

def hist_render(ticker, startdate, enddate):
    weekdays_list = ["MON", "TUE", "WED", "THU", "FRI"]
    response_data = {}
    for weekday in weekdays_list:
        response_data[weekday] = {}
        q1 = Historical.objects.filter(ticker=ticker).filter(date__gte=startdate).filter(date__lte=enddate).filter(weekday=weekday)
        response_data[weekday]['overnight'] = float(round(q1.aggregate(Avg('overnight'))['overnight__avg'], 2))
        response_data[weekday]['intraday'] = float(round(q1.aggregate(Avg('intraday'))['intraday__avg'], 2))
        response_data[weekday]['sum24'] = float(round(q1.aggregate(Avg('sum24'))['sum24__avg'], 2))
        response_data[weekday]['vol'] = float(round(q1.aggregate(Avg('volume'))['volume__avg'], 2))
        td = q1.count()
        response_data[weekday]['on_pm'] = round((q1.filter(overnight__gt=0).count()) / (td / 100))
        response_data[weekday]['id_pm'] = round((q1.filter(intraday__gt=0).count()) / (td / 100))
        response_data[weekday]['sum_pm'] = round((q1.filter(sum24__gt=0).count()) / (td / 100))
    return response_data