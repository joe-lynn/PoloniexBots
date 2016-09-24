import csv
import os.path
import time

from api.poloniex_wrapper import poloniex
from constants.api_key import API_KEY, SECRET_KEY
from constants.poloniex_constants import LOAN_CURRENCIES

OUTFILE = 'data/test.csv'
WRITE_INTERVAL = 180
FIELD_NAMES = ['currency', 'rate', 'amount', 'rangeMax', 'rangeMin']
DEFAULT_LOAN = {'rate': 0.05, 'amount': 0, 'rangeMax': -1, 'rangeMin': -1}

# TODO(pallarino): Need to catch key exception if there are no loan offers

class NaiveLender():
	def __init__(self, polo):
		self.polo = polo
		if not os.path.exists(OUTFILE):
			with open(OUTFILE, 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES, delimiter=',')
				writer.writeheader()

	def run_indef(self):
		while True:
			print 'Awake!'
			with open(OUTFILE, 'a') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES, delimiter=',')
				
				for currency in LOAN_CURRENCIES:
					try:
						orders = self.polo.returnLoanOrders(currency)
					# Need to catch various connection exceptions here.
					except Exception, e:
						print e

					try:
						open_offers = orders['offers']
					except KeyError, k:
						print "KeyError occurred, no loan offers found."
						open_offers = [DEFAULT_LOAN]

					try:
						lowest_offer = open_offers[0]
					except IndexError, i:
						print "IndexError occurred, no loan offers returned"
						lowest_offer = DEFAULT_LOAN

					offer = {'currency': currency}
					offer['rate'] = lowest_offer['rate']
					offer['amount'] = lowest_offer['amount']
					offer['rangeMax'] = lowest_offer['rangeMax']
					offer['rangeMin'] = lowest_offer['rangeMin']

					print 'Writing.'
					writer.writerow(offer)
			print 'Sleeping...'
			time.sleep(WRITE_INTERVAL)
		


