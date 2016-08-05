import math

X_CURRENCY = 'ETH'

BTC_X_INCREMENT = 0.000001
BTC_X_START_PRICE = 0.001
BTC_X_END_PRICE = 0.1

USDT_X_INCREMENT = 0.001
USDT_X_START_PRICE = 1
USDT_X_END_PRICE = 100

USDT_BTC_INCREMENT = 0.01
USDT_BTC_START_PRICE = 10
USDT_BTC_END_PRICE = 1000


BTC_X_PAIR = 'BTC' + X_CURRENCY
USDT_X_PAIR = 'USDT' + X_CURRENCY
USDT_BTC_PAIR = 'USDT_BTC'

current_btc_x = BTC_X_START_PRICE
current_usdt_x = USDT_X_START_PRICE
current_usdt_btc = USDT_BTC_START_PRICE

def get_distance(point1, point2):
	# Returns the absolute distance between two points (x1, x2, x3) and (y1, y2, y3)
	return abs(math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point[3])**2))

def find_normal_vector(market_point):
	perfect_point = (BTC_X_START_PRICE, USDT_BTC_START_PRICE, BTC_X_START_PRICE*USDT_BTC_START_PRICE)
	old_point = (perfect_point[0], perfect_point[1], perfect_point[2])
	new_point = (0,0,0)
	old_distance = get_distance(market_point, perfect_point)
	new_distance = -10000
	while new_distance < old_distance:
		old_distance = new_distance
		p1 = (old_point[0] + BTC_X_INCREMENT, old_point[1], old_point[2])
		p2 = (old_point[0], old_point[1] + USDT_BTC_INCREMENT, old_point[2])
		p3 = (old_point[0], old_point[1], old_point[2] + USDT_X_INCREMENT)
		d1 = get_distance(old_point, p1)
		d2 = get_distance(old_point, p2)
		d3 = get_distance(old_point, p3)
		new_distance = d1
		new_point = p1
		if d2 < new_distance:
			new_distance = d2
			new_point = p2
		if d3 < new_distance:
			new_distance = d3
			new_point = p3
		





def generate_cache():	
	current_btc_x = BTC_X_START_PRICE
	while current_btc_x < BTC_X_END_PRICE:
		current_btc_x += BTC_X_INCREMENT
		current_usdt_btc = USDT_BTC_START_PRICE
		while current_usdt_btc < USDT_BTC_END_PRICE:
			current_usdt_btc += USDT_BTC_INCREMENT
			current_usdt_x = USDT_X_START_PRICE
			while current_usdt_x < USDT_X_END_PRICE:
				current_usdt_x += USDT_X_INCREMENT
				# Send the point in this form because the third is always alone in the equation
				# USDT/X = BTC/X * USDT/BTC
				point = (current_btc_x, current_usdt_btc, current_usdt_x)
				find_normal_vector(point)
				return
		
			

#generate_cache()
print("done")