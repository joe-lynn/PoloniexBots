import threading
import time
import poloniex_constants
from poloniex_wrapper import poloniex
from arbitrager import usd_arbitrager

polo = poloniex(API_KEY, SECRET_KEY)

# Searches for arbitrage opportunities in a triangle between BTC, another crypto X, and USDT.
def find_arbitrage_BTC_X_USDT(btc_x_pair, usdt_x_pair):
	arbitrager = usd_arbitrager(polo, btc_x_pair, usdt_x_pair)
	arbitrager.start()

find_arbitrage_BTC_X_USDT('BTC_ETH', 'USDT_ETH')
