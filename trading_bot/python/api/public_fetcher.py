
import threading

class public_fetcher(threading.Thread):
	def __init__(self, polo):
		super().__init__()
		self.polo = polo

	def get_loan_offers(self, currency):

	def run(self):