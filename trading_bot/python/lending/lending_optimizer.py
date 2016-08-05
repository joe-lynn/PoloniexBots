# NOTE: Currently this bot just undercuts the lowest offer and places everything for that price
# to avoid downtime. However, if in the future we could have a good predictor of lending rates
# this algorithm would change. 

import requests
import threading
import time

from api_key import *
from poloniex_wrapper import poloniex
from poloniex_constants import *

# Computes the number of days to offer the loan at based on the loan rate.
# This will start with a linear mapping but will later change to be based on historic
# values (i.e. relative to the usual rate).
#
# We map the percentage of the max lending rate to the percentage of the max days.
def compute_lending_days(lending_rate):
	percent_adjustment = 1 - ((MAX_LENDING_RATE - lending_rate) / LENDING_RATE_DIF)
	day_adjustment = percent_adjustment * LENDING_DAYS_DIF
	return MIN_LENDING_DAYS + day_adjustment

class lender(threading.Thread):
	def __init__(self, polo):
		super().__init__()
		self.polo = polo
		self.rates_file = open("~/Code/trading_bot/min_rates.dat", 'a')
		
	def update_minimum_rates




	# polo.returnOpenLoanOffers() - balances not in account and not on loan
	# polo.returnActiveLoans() - balances on loan
	# polo.returnAvailableAccountBalanes
	def update_loans(self):
		# TODO: Create a cache for these values once upon construction and add as we create offers.
		# This allows us to whitelist orders that are already on the books.
		open_offers = polo.returnOpenLoanOffers()
		for currency in LOAN_CURRENCIES:
			if currency not in open_offers:
				continue
			for offer in open_offers[currency]:
				if float(offer['rate']) < MIN_LENDING_RATE * 10:
					continue
				polo.cancelLoanOffer(offer['id'])

		time.sleep(2)

		# TODO: More sophisticated calculation of loan rate.
		balances = polo.returnAvailableAccountBalances('lending')['lending']
		for currency in LOAN_CURRENCIES:
			time.sleep(0.50)
			if currency not in balances:
				continue
			elif float(balances[currency]) < MIN_LENDING_AMOUNT:
				continue
			lowest_offer = self.polo.returnLoanOrders(currency)['offers'][0]
			rate = round(float(lowest_offer['rate']) - 0.00000001, 8)
			if rate < MIN_LENDING_RATE:
				rate = MIN_LENDING_RATE * 10

			print("Creating loan offer: ", end="")
			loan_offer = {'currency': currency, 'amount': balances[currency], 'duration': compute_lending_days(rate), 'autoRenew': 0, 'lendingRate': rate}
			print(loan_offer)

			ret = polo.createLoanOffer(currency, balances[currency], rate, compute_lending_days(rate), 0)

			print(ret)

	def run(self):
		while True:
			try:
				self.update_loans()
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
			time.sleep(15)
			


polo = poloniex(API_KEY, SECRET_KEY)
lender = lender(polo)
lender.start()