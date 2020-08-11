# Stock Market App
A website with two apps:
1. Historical: Checks any stock for past year open, close, and volume daily performance and displays stats based on day of the week.
    Range within the year is customizable.
2. Options Log: Displays all past options trades along with stats for each ticker (or all tickers) and each option type (or both).
    Currently only supports uploads from WeBull.
---
## Historical
### Features
- Four forms that request yfinance API through Django server and receive formatted data (stats) to display on main page
### Todo
- [x] Use one JS function for all tables instead of copypasting 99% of the function for each table
- [ ] Link Historical app to Options Log app via navbar link
- [ ] Change color of most prominent stats based on value
- [x] Possible idea: add list of all transactions within date range under table
### Notes
 - 08/08/2020 - Gotta redo most of the system, sort of an abandoned app as of now. Possible next move is to remove database altogether and just pull info from yfinance directly every time.
 - 08/09/2020 - Completely deleted database and models, used JS fetch to request data, and basic Python to get yfinance API data and feed it back for JS to render it in page without reloading. Does exactly what I set out to accomplish.
 - 08/10/2020 - Adjusted everything for hosting on Heroku. Added a list of days for each selected range, made a hide button for it. Adjusted a lot of CSS. Python looks pretty good. CSS looks very serviceable. JS looks worse than ever, hardcoded everything in the longest way possible.

---
## Options Log
### Features
- Basic login system
- Navigation bar
- Upload page where WeBull downloaded trade history (csv format) can be copypasted into a textarea
- Main page displays open trades and all transactions
- Main page also displays a working form that displays stats based on customizable parameters
### Todo
- [x] Learn how to add `login_required` decorator
- [x] Figure out best system for positions that just expire without being sold (button to manually refresh them vs. Checking automatically somehow)
- [x] Reform models.py/schema and option details into Contract rather than Transaction, then reflect changes on views.py and index.html
- [x] Format 'open positions' div into a table (after fixing database)
- [x] Figure out how to update 'profit' field on navigation bar (refresh button vs. auto)
- [ ] Instructions page for WeBull upload with images
- [x] Favicon
- [ ] ~~Paginate transactions list on the right~~
- [ ] Set transactions list height and make it scrollable
- [ ] Fix commented lines in index.html to add Select Option placeholders and JS script for enabling and disabling Submit button
- [ ] Future - Optimize index_helper function (shows main page stats from form POST). Since only 4 possible results, each is currently hard-coded
- [ ] Future - Chart representation for stats
- [ ] Future - Sort/filter for tables
- [ ] Future - Allow upload from other brokers
### Notes
 - 08/08/2020 - After getting the backend to work, I realized my schema was backwards. Details such as option ticker, expiration date, option type, and strike should be in the Contract object, not in every single Transaction object. Since it does work as of now, I'm pushing this version and then redoing the whole database and everything directly affected by it. That's the main focus now.
 - 08/09/2020 - New database structure finalized yesterday plus a few TODOs. Everything works according to plan and it does what I wanted it to do when I created the app. There's still plenty to improve with JS and the index_helper function, along with side goals and future features.