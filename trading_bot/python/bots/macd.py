import sys
sys.path.append("/Users/Timothy/Code/Poloniex/trading_bot/python")

import requests
import threading
import imp
import time

from api.poloniex_wrapper import poloniex
from constants.api_key import API_KEY, SECRET_KEY
#poloniex

class macd_bot(threading.Thread):
	def __init__(self, polo, pair):
		super().__init__()
		self.polo = polo
		self.currency_pair = pair
		self.period = int(300) # Start with the 5 minute candles to test

	def trade_macd(self):
		end_time = int(time.time())
		print("end:   " + str(end_time))
		start_time = int(end_time - self.period * 10)
		print("start: " + str(start_time))
		ret = self.polo.returnChartData(self.currency_pair, self.period, start_time, 9999999999)
		print(ret)

	def run(self):
		while True:
			try:
				self.trade_macd()
			except requests.exceptions.HTTPError as e:
				print("HTTP Exception Caught!!")
				continue
			except KeyError as e:
				print(e)
				print("KeyError Caught!!")
				continue
			except ValueError as e:
				print(e)
				print("ValueError Caught!!")
			except requests.exceptions.ConnectionError as e:
				print(e)
				time.sleep(100)
				self.polo = poloniex(API_KEY, SECRET_KEY)
				print("ConnectionError Caught!!")
			print("Sleeping...")
			time.sleep(1)


polo = poloniex(API_KEY, SECRET_KEY)
macd = macd_bot(polo, 'BTC_XMR')
macd.start()