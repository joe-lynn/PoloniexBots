import math
# (BTC/X, USDT/BTC, USDT/X)

BTC_X_INCREMENT = 0.0001
USDT_BTC_INCREMENT = 0.0001
INCREMENT_AMOUNT = 0.000005

def get_distance(market_point, surface_point):
	return math.sqrt((market_point[0] - surface_point[0])**2 + (market_point[1] - surface_point[1])**2 + (market_point[2] - surface_point[2])**2)
	
def get_min_distance_point(ref_point, p1, p2, p3, p4):
	min_distance_point = ref_point
	if p1[0] < min_distance_point[0]:
		min_distance_point = p1
	if p2[0] < min_distance_point[0]:
		min_distance_point = p2
	if p3[0] < min_distance_point[0]:
		min_distance_point = p3
	if p4[0] < min_distance_point[0]:
		min_distance_point = p4
	return min_distance_point
	
def get_closest_point(market_point):
	perfect_point = (market_point[0], market_point[1], market_point[0] * market_point[1])
	reference_point = perfect_point
	
	BTC_X_INCREMENT = INCREMENT_AMOUNT * market_point[0]
	USDT_BTC_INCREMENT = INCREMENT_AMOUNT * market_point[1]
	STEP_SIZE = min(BTC_X_INCREMENT, USDT_BTC_INCREMENT)
	
	
	point_1 = (perfect_point[0] + STEP_SIZE, perfect_point[1], (perfect_point[0] + STEP_SIZE) * perfect_point[1])
	point_2 = (perfect_point[0] - STEP_SIZE, perfect_point[1], (perfect_point[0] - STEP_SIZE) * perfect_point[1])
	point_3 = (perfect_point[0], perfect_point[1] + STEP_SIZE, perfect_point[0] * (perfect_point[1] + STEP_SIZE))
	point_4 = (perfect_point[0], perfect_point[1] - STEP_SIZE, perfect_point[0] * (perfect_point[1] - STEP_SIZE))
	
	ref = (get_distance(market_point, reference_point), reference_point)
	dp1 = (get_distance(market_point, point_1), point_1)
	dp2 = (get_distance(market_point, point_2), point_2)
	dp3 = (get_distance(market_point, point_3), point_3)
	dp4 = (get_distance(market_point, point_4), point_4)
	
	previous_point = ref
	current_point = get_min_distance_point(ref, dp1, dp2, dp3, dp4)
	while current_point[0] != previous_point[0]:
		# Set the current distance-point pair to the previous
		previous_point = current_point
		# Compute the new points
		point_1 = (previous_point[1][0] + STEP_SIZE, previous_point[1][1], (previous_point[1][0] + STEP_SIZE) * previous_point[1][1])
		point_2 = (previous_point[1][0] - STEP_SIZE, previous_point[1][1], (previous_point[1][0] - STEP_SIZE) * previous_point[1][1])
		point_3 = (previous_point[1][0], previous_point[1][1] + STEP_SIZE, previous_point[1][0] * (previous_point[1][1] + STEP_SIZE))
		point_4 = (previous_point[1][0], previous_point[1][1] - STEP_SIZE, previous_point[1][0] * (previous_point[1][1] - STEP_SIZE))
		
		# Compute the distances for each of these points
		dp1 = (get_distance(market_point, point_1), point_1)
		#print(dp1)
		dp2 = (get_distance(market_point, point_2), point_2)
		#print(dp2)
		dp3 = (get_distance(market_point, point_3), point_3)
		#print(dp3)
		dp4 = (get_distance(market_point, point_4), point_4)
		#print(dp4)
		
		# Find the point with the minimum distance from the market point
		current_point = get_min_distance_point(previous_point, dp1, dp2, dp3, dp4)
		print(current_point)

	return current_point[1]
	
market_point = (0.02233, 446, 9.902)
perfect_point = get_closest_point(market_point)
dif_vector = (perfect_point[0] - market_point[0], perfect_point[1] - market_point[1], perfect_point[2] - market_point[2])
print(dif_vector)

dot_prod = dif_vector[0] * perfect_point[1] + dif_vector[1] * perfect_point[0] + dif_vector[2] * (math.sqrt(perfect_point[0]**2 + perfect_point[1]**2))
print(dot_prod)