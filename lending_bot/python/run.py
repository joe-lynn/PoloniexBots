import sys

sys.path.insert(0, '/Users/Timothy/Code/PoloniexBots/lending_bot/python')

from bots.naive_lender import NaiveLender
from api.poloniex_wrapper import poloniex
from constants.api_key import API_KEY, SECRET_KEY

if __name__ == '__main__':
	polo = poloniex(API_KEY, SECRET_KEY)
	l = NaiveLender(polo)
	l.run_indef()
