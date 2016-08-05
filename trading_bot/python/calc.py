MAKER_FEE = 0.9985
TAKER_FEE = 0.9975

buying_fee = TAKER_FEE
selling_fee = MAKER_FEE

buying_price = 0.00073560
selling_price = 2206

buying_amt = 203.915
selling_amt = 23.84975671

holdover_amt = 0.024
holdover_pct = 1

percent = True

def sell_to_buy(percent = False):
	# Start with 100 selling amount
	print("Sell to Buy")

	# Convert the holdover amount to make this easier
	if percent:
		converted_holdover_amt = (holdover_pct / 100.0) * selling_price * selling_amt
	else:
		converted_holdover_amt = holdover_amt * selling_price # In this case, it is 0.25
	# Convert the selling amount
	conv_sell_amt = selling_amt * selling_price # In this case, it is 1.00
	# Apply fees to get how much we actually received from the sale
	conv_sell_amt_post_fee = conv_sell_amt * selling_fee # In this case, it is 0.50
	# Take the holdover amount away from how much we received. This is effectively how much we have to rebuy
	conv_sell_amt_post_hold = conv_sell_amt_post_fee - converted_holdover_amt # In this case, it is 0.25
	# We now need to figure out the price at which we can end with 100 of the old currency
	# We  have that (amt / price) * fees = 100, so price = (amt * fees) / 100
	rebuy_price = (conv_sell_amt_post_hold * buying_fee) / selling_amt
	print("Rebuy Price: " + str(rebuy_price))
	print("Rebuy Amount: " + str(selling_amt / buying_fee))


def buy_to_sell(percent = False):
	# We want to buy 100 at 0.01
	print("Buy to Sell")

	# This is the amount we are paying for such a trade
	conv_buy_amt = buying_amt * buying_price # In this case, it is 1.0

	# This is the amount we are actually receiving, after fees
	buy_amt_after_fees = buying_amt * buying_fee # In this case, it is 50

	# This is the amount we have to resell, after holdover
	if percent:
		buy_amt_after_hold = buy_amt_after_fees - (holdover_pct * buying_amt / 100.0) # In this case, it is 25
	else:
		buy_amt_after_hold = buy_amt_after_fees - holdover_amt # In this case, it is 25

	# We want to sell this amount and end up with the same amount as the conv_buy_amt
	# So we have (amt * price * fees) = conv_buy_amt, so price = conv_buy_amt / (amt * fees)
	resell_price = conv_buy_amt / (buy_amt_after_hold * selling_fee)
	print("Resell Price: " + str(resell_price))
	print("Resell Amount: " + str(conv_buy_amt / (resell_price * selling_fee)))

sell_to_buy(percent)
buy_to_sell(percent)