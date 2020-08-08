import yfinance as yf

qqq = yf.Ticker("QQQ")
hist = qqq.history(period="1y")

logo = "https://storage.googleapis.com/iex/api/logos/" + symbol + ".png"

# Set first overnight to 0 by matching non-existing close to first open
lastclose = hist.at[hist.index[0], 'Open']

overnight_count = 0
intraday_count = 0
sum24_count = 0
day_count = 0

days_of_week = {
    1: "MON",
    2: "TUE",
    3: "WED",
    4: "THU",
    5: "FRI"
}

for date in hist.index:
    weekday = days_of_week[date.weekday()]
    date = str(date)[:-9]
    priceopen = hist.at[date, 'Open']
    priceclose = hist.at[date, 'Close']
    overnight = '{0:.0%}'.format((priceopen - lastclose) / lastclose)
    intraday = '{0:.0%}'.format((priceclose - priceopen) / priceopen)
    sum24 = '{0:.0%}'.format((priceclose - lastclose) / lastclose)
    volume = hist.at[date, 'Volume']
    high = hist.at[date, 'High']
    low = hist.at[date, 'Low']

    if overnight > 0:
        overnight_count += 1
    if intraday > 0:
        intraday_count += 1
    if sum24 > 0:
        sum24_count += 1

    day_count += 1
    lastclose = priceclose

    if day_count == 250:
        print(date, weekday)