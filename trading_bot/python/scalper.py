import threading

from poloniex_constants import *
from poloniex_wrapper import poloniex
from arbitrager import usd_arbitrager

SCALP_AMOUNT = 0.1

class scalper(threading.Thread):
	def __init__(self, pair):
		super().__init__()
		self.currency_pair = pair
		self.current_bid = {'currencyPair':pair, 'rate':0, 'amount':0, 'orderNumber':0}
		self.current_ask = {'currencyPair':pair, 'rate':0, 'amount':0, 'orderNumber':0}

	# Need to adjust algorithm to avoid race conditions
	def scalp(self, order_book):
		asks = order_book['asks']
		bids = order_book['bids']

		# Later, we will add more sophistocated stuff to check the actual order volume
		# For now, however, we will simply look for advantageous spreads
		lowest_ask = asks[0]
		lowest_ask_price = float(lowest_ask[0])
		highest_bid = bids[0]
		highest_bid_price = float(highest_bid[0])

		scalp_bid = round(highest_bid_price + 0.00000001, 8)
		scalp_ask = round(lowest_ask_price - 0.00000001, 8)

		# Here's what's happening, we are allowed to have only 1 sell and 1 buy on the order books at any given time
		# for any given pair that we are scalping (subject to change since we might also be trading it randomly)
		# Basically we need to check the scalp bid and ask.
		# If we have no orders on the books, place them
		# Otherwise, we need to check if these prices are different than ours
		# If so we need to cancel the orders that differ and replace them


		# TODO:
		# Need to check if we currently have orders on the books
		open_orders = polo.returnOpenOrders(self.currency_pair)
		print(open_orders)
		if not open_orders:
			print("Orders are empty")
		# If so, we want to move our order up if it's still profitable
		# or move it back if the order we were cutting has moved back
		# If not, then check if it's profitable and place orders accordingly

		if scalp_ask * M_FEE_ONE > scalp_bid:
			# Ayyy lmao, we found a scalping opportunity
			print("Bid: " + str(scalp_bid))
			print("Ask: " + str(scalp_ask))

			ask_trade = {'currencyPair':self.currency_pair, 'rate':scalp_ask, 'amount':SCALP_AMOUNT}
			bid_trade = {'currencyPair':self.currency_pair, 'rate':scalp_bid, 'amount':SCALP_AMOUNT}

			ask_response = polo.sell(ask_trade['currencyPair'], ask_trade['rate'], ask_trade['amount'])
			bid_response = polo.buy(bid_trade['currencyPair'], bid_trade['rate'], bid_trade['amount'])

			if 'error' not in ask_response:
				self.current_ask = scalp_ask
			else:
				polo.cancel(self.currency_pair, bid_response['orderNumber'])

			if 'error' not in bid_response:
				self.current_bid = scalp_bid
			else:
				polo.cancel(self.currency_pair, ask_response['orderNumber'])





polo = poloniex(API_KEY, SECRET_KEY)

scalper = scalper('BTC_DASH')
scalper.scalp(polo.returnOrderBook('BTC_DASH'))
