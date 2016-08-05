from poloniex_constants import *
import math

def find_surface_point(p0, p1):
	print(p0)
	print(p1)
	dB = p1[0] - p0[0]
	dy = p1[1] - p0[1]
	dz = p1[2] - p0[2]

	a = dB * dy
	b = dy * p0[0] + dB * p0[1] - dz
	c = p0[0] * p0[1] - p0[2]
	t0 = (-b + math.sqrt((b**2) - (4 * a * c))) / (2 * a)
	t1 = (-b - math.sqrt((b**2) - (4 * a * c))) / (2 * a)

	sp0 = (p0[0] + dB * t0, p0[1] + dy * t0, p0[2] + dz * t0)
	sp1 = (p0[0] + dB * t1, p0[1] + dy * t1, p0[2] + dz * t1)

	#print(sp0)
	#print(sp0[0]*sp0[1]/sp0[2])
	#print(sp1)
	#print(sp1[0]*sp1[1]/sp1[2])

	if sp0[0] >= 0 and sp0[1] > 0 and sp0[2] > 0:
		return sp0
	else:
		return sp1

def find_arbitrage(A_B_book, C_A_book, C_B_book):
	print("Searching...")
	# Grab all of the order books and get either the highest bid or lowest ask.
	A_B_ask = A_B_book['asks'][0]
	A_B_bid = A_B_book['bids'][0]
	C_A_ask = C_A_book['asks'][0]
	C_A_bid = C_A_book['bids'][0]
	C_B_ask = C_B_book['asks'][0]
	C_B_bid = C_B_book['bids'][0]

	# Assume we begin at A, then there are two routes to take to return to A.
	# First Cycle: A -> B -> C -> A
	# Step 1: We have A and we want to buy B, so we need to look at the lowest ask.
	# Step 2: We have B and we want to sell B, so we need to look at the highest bid.
	# Step 3: We have C and we want to buy A, so we need to look at the lowest ask.
	c1_price_1 = float(A_B_ask[0])
	c1_price_2 = float(C_B_bid[0])
	c1_price_3 = float(C_A_ask[0])
	c1_amt_1 = float(A_B_ask[1])
	c1_amt_2 = float(C_B_bid[1])
	c1_amt_3 = float(C_A_ask[1])

	profit_cycle_1 = (1.0 / c1_price_1) * c1_price_2 * (1.0 / c1_price_3) * T_FEE_THREE
	print(profit_cycle_1)
	# If it is greater than 1, we've found a profit opportunity
	if profit_cycle_1 > 1.0:
		# Will have some debug strings here for a while to test.
		print("Arbitrage Opportunity Found: ")
		print(A_B_ask)
		print(C_B_bid)
		print(C_A_ask)

		print("Adjusted BTC Amounts: ")
		adj_btc_amt_1 = c1_price_1 * c1_amt_1
		print("Adjusted Amount 1: " + str(adj_btc_amt_1))
		adj_btc_amt_2 = c1_price_1 * c1_amt_2 * T_INV_FEE_ONE
		print("Adjusted Amount 2: " + str(adj_btc_amt_2))
		adj_btc_amt_3 = c1_price_1 * (1.0 / c1_price_2) * c1_price_3 * c1_amt_3 * T_INV_FEE_TWO
		print("Adjusted Amount 3: " + str(adj_btc_amt_3))

		arb_amt = min(adj_btc_amt_1, adj_btc_amt_2, adj_btc_amt_3)
		print("Arbitrage Amount: " + str(arb_amt))

		trade_amt_1 = arb_amt / c1_price_1
		trade_amt_2 = (arb_amt / c1_price_1) * T_FEE_ONE
		trade_amt_3 = (trade_amt_2 * T_FEE_ONE * c1_price_2) / c1_price_3

#		trade_1 = {'currencyPair':self.BTC_X, 'rate':str(price_1), 'amount':str(trade_amt_1)}
#		trade_2 = {'currencyPair':self.USDT_X, 'rate':str(price_2), 'amount':str(trade_amt_2)}
#		trade_3 = {'currencyPair':self.USDT_BTC, 'rate':str(price_3), 'amount':str(trade_amt_3)}

		return ({'rate':str(c1_price_1), 'amount':str(trade_amt_1)}, {'rate':str(c1_price_2), 'amount':str(trade_amt_2)}, {'rate':str(c1_price_3), 'amount':str(trade_amt_3)})


	# Second Cycle: A -> C -> B -> A
	# Step 1: We have A and we want to sell A, so we need to look at the highest bid.
	# Step 2: We have C and we want to buy B, so we need to look at the lowest ask.
	# Step 3: We have B and we want to sell B, so we need to look at the highest bid.
	c2_price_1 = float(C_A_bid[0])
	c2_price_2 = float(C_B_ask[0])
	c2_price_3 = float(A_B_bid[0])
	c2_amt_1 = float(C_A_bid[1])
	c2_amt_2 = float(C_B_ask[1])
	c2_amt_3 = float(A_B_bid[1])

	profit_cycle_2 = c2_price_1 * (1.0 / c2_price_2) * c2_price_3 * T_FEE_THREE
	print(profit_cycle_2)

	# If it is greater than 1, we've found a profit opportunity
	if profit_cycle_2 > 1.0:
		# Will have some debug strings here for a while to test.
		print("Arbitrage Opportunity Found: ")
		print(C_A_bid)
		print(C_B_ask)
		print(C_A_bid)

		print("Adjusted BTC Amounts: ")
		adj_btc_amt_1 = c2_amt_1
		print("Adjusted Amount 1: " + str(adj_btc_amt_1))
		adj_btc_amt_2 = (c2_amt_2 * c2_price_2) / (T_FEE_ONE * c2_price_1)
		print("Adjusted Amount 2: " + str(adj_btc_amt_2))
		adj_btc_amt_3 = (c2_amt_3 * c2_price_2) / (c2_price_1 * T_FEE_TWO)
		print("Adjusted Amount 3: " + str(adj_btc_amt_3))

		arb_amt = min(adj_btc_amt_1, adj_btc_amt_2, adj_btc_amt_3)
		print("Arbitrage Amount: " + str(arb_amt))

		trade_amt_1 = arb_amt
		trade_amt_2 = (arb_amt * c2_price_1 * T_FEE_ONE) / c2_price_2
		trade_amt_3 = (arb_amt * c2_price_1 * T_FEE_TWO) / c2_price_2

#		trade_1 = {'currencyPair':self.USDT_BTC, 'rate':str(price_1), 'amount':str(trade_amt_1)}
#		trade_2 = {'currencyPair':self.USDT_X, 'rate':str(price_2), 'amount':str(trade_amt_2)}
#		trade_3 = {'currencyPair':self.BTC_X, 'rate':str(price_3), 'amount':str(trade_amt_3)}

		return ({'rate':str(c2_price_1), 'amount':str(trade_amt_1)}, {'rate':str(c2_price_2), 'amount':str(trade_amt_2)}, {'rate':str(c2_price_3), 'amount':str(trade_amt_3)})

	return None