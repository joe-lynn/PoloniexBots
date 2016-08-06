import api.public_fetcher
import os
import signal
import sys
import threading


sys.path.append("/Users/Timothy/Code/Poloniex/trading_bot/python")

class stat_writer(threading.Thread):
	def write_stats(self):
		lock.acquire()
		# TODO(pallarino): Loop through loan currencies and write to respective files.
		fetcher.get_loan_offers()
		rates_file.write()
		lock.release()

	def __init__(self, fetcher):
		super().__init__()
		self.rates_file = open("./data/min_rates.dat", 'a')
		self.lock = threading.Lock()
		signal.signal(signal.SIGALRM, write_stats)
		self.fetcher = fetcher

	def run(self):
		time.sleep(0)