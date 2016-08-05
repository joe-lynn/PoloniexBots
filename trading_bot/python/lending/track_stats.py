import threading


class stat_writer(threading.Thread):
	def __init__(self):
		super().__init__()
		self.rates_file = open("~/Code/trading_bot/min_rates.dat", 'a')
		self.lock = threading.Lock()

	def run(self):
		