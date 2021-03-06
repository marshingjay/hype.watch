# JACOB MARSHALL 2020 :)

from datetime import datetime
import time
import csv
from config import *
from pathlib import Path
import alpaca_trade_api as alpaca

def set_watchlist(my_list, filename):
    my_list.clear()
    my_watchlist = open(filename, 'r')
    for symbol in my_watchlist:
        my_list.add(symbol.replace('\n', ''))


# set up API
api = alpaca.REST(API_KEY, SECRET_KEY, ENDPOINT_URL)
clock = api.get_clock()

# set up watchlist
watchlist = set()
previous_size = Path('watchlist.hype').stat().st_size
set_watchlist(watchlist, 'watchlist.hype')

hypelist = set()

# book-keeping
next_cycle = False
last_minute = datetime.now().minute
cur_size = 0

#check if market is open
if not clock.is_open:
    print('market is closed!')

#main loop
while True:
    #check if file has been changed
    cur_size = Path("watchlist.hype").stat().st_size
    if cur_size != previous_size:
        previous_size = cur_size
        set_watchlist(watchlist, 'watchlist.hype')


    for symbol in hypelist:
        data = api.get_barset(symbol, 'day', limit=2)
        yesterday_close = data[symbol][0].c
        data = api.get_barset(symbol, 'minute', limit=2)
        last_minute_price = data[symbol][0].c
        this_minute_price = data[symbol][1].c
        if this_minute_price < last_minute_price:
            print('ALERT: ' + symbol + ' is now only up ' + str((this_minute_price / yesterday_close * 100) - 100) + '%, down ' + str(last_minute_price-this_minute_price) + ' in the last minute')
    #do price comparisons on each stock
    for symbol in watchlist:
        data = api.get_barset(symbol, 'day', limit=2)
        yesterday_close = data[symbol][0].c
        data = api.get_barset(symbol, 'minute', limit=1)
        cur_price = data[symbol][0].c
        if cur_price >= 1.15 * yesterday_close:
            print('ALERT: ' + symbol + ' has increased by ' + str((cur_price / yesterday_close * 100) - 100) + '% and is now at ' + str(cur_price) + ' (closed yesterday at ' + str(yesterday_close) + ')')
            hypelist.add(symbol)
    #wait until exactly a minute has passed since the last loop began and then go again
    this_minute = datetime.now().minute
    while last_minute == this_minute:
        time.sleep(1)
        this_minute = datetime.now().minute
    last_minute = this_minute



