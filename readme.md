# Stock Market App
A website with two apps:
1. Historical: Checks any stock for past year open, close, and volume daily performance and displays stats based on day of the week.
    Range within the year is customizable.
2. Options Log: Displays all past options trades along with stats for each ticker (or all tickers) and each option type (or both).
    Currently only supports uploads from WeBull.
---
## Historical
### Features
- A few
### Todo
- [ ] A lot
### Notes
08/08/2020 - Gotta redo most of the system, sort of an abandoned app as of now. Possible next move is to remove database altogether and just pull info from yfinance directly every time.

---
## Options Log
### Features
- Basic login system
- Navigation bar
- Upload page where WeBull downloaded trade history (csv format) can be copypasted into a textarea
- Main page displays open trades and all transactions
- Main page also displays a working form that displays stats based on customizable parameters
### Todo
- [ ] Learn how to add `login_required` decorator
- [ ] Figure out best system for positions that just expire without being sold (button to manually refresh them vs. Checking automatically somehow)
- [x] Reform models.py/schema and option details into Contract rather than Transaction, then reflect changes on views.py and index.html
- [x] Format 'open positions' div into a table (after fixing database)
- [x] Figure out how to update 'profit' field on navigation bar (refresh button vs. auto)
- [ ] Instructions page for WeBull upload with images
- [ ] Paginate transactions list on the right
- [ ] Future - Optimize index_helper function (shows main page stats from form POST). Since only 4 possible results, each is currently hard-coded
- [ ] Future - chart representation for stats
- [ ] Future - sort/filter for tables
### Notes
08/08/2020 - After getting the backend to work, I realized my schema was backwards. Details such as option ticker, expiration date, option type, and strike should be in the Contract object, not in every single Transaction object. Since it does work as of now, I'm pushing this version and then redoing the whole database and everything directly affected by it. That's the main focus now.