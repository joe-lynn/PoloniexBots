import threading

from perfect_market_util import *
from poloniex_wrapper import poloniex
from poloniex_constants import *

class usd_arbitrager(threading.Thread):
	def __init__(self, polo, btc_x, usdt_x):
		super().__init__()
		self.polo = polo
		self.BTC_X = btc_x
		self.USDT_X = usdt_x
		self.USDT_BTC = 'USDT_BTC'

	def find_trades(self, BTC_X_book, USDT_BTC_book, USDT_X_book):
		# TODO: If we are only going to use the lowest ask and highest bid, we can just return the ticker.
		# This should hopefulyl be shorter than 3 API calls
		# Grab all of the order books and get either the highest bid or lowest ask.
		BTC_X_ask = BTC_X_book['asks'][0]
		BTC_X_bid = BTC_X_book['bids'][0]
		USDT_BTC_ask = USDT_BTC_book['asks'][0]
		USDT_BTC_bid = USDT_BTC_book['bids'][0]
		USDT_X_ask = USDT_X_book['asks'][0]
		USDT_X_bid = USDT_X_book['bids'][0]
		trade = find_arbitrage(BTC_X_book, USDT_BTC_book, USDT_X_book)
		if trade is not None:
			trade_1 = {'currencyPair':self.BTC_X, 'rate':trade[0]['rate'], 'amount':trade[0]['amount']}
			trade_2 = {'currencyPair':self.USDT_X, 'rate':trade[1]['rate'], 'amount':trade[1]['amount']}
			trade_3 = {'currencyPair':self.USDT_BTC, 'rate':trade[2]['rate'], 'amount':trade[2]['amount']}

		p0 = (float(BTC_X_bid[0]), float(USDT_BTC_bid[0]), float(USDT_X_ask[0]))
		p1 = (float(BTC_X_ask[0]), float(USDT_BTC_ask[0]), float(USDT_X_bid[0]))
		surface_point = find_surface_point(p0, p1)
		

	def run(self):
		while True:
			try:
				BTC_X_book = self.polo.returnOrderBook(self.BTC_X) # Map of (price in BTC/X) : (# X in order)
			except requests.exceptions.HTTPError as e:
				print("Exception Handled!!")
				continue
			try:
				USDT_BTC_book = self.polo.returnOrderBook(self.USDT_BTC) # Map of (price in USDT/BTC) : (# BTC in order)
			except requests.exceptions.HTTPError as e:
				print("Exception Handled!!")
				continue
			try:
				USDT_X_book = self.polo.returnOrderBook(self.USDT_X) # Map of (price in USDT/X) : (# X in order)
			except requests.exceptions.HTTPError as e:
				print("Exception Handled!!")
				continue

			self.find_trades(BTC_X_book, USDT_BTC_book, USDT_X_book)