import math

def find_surface_point(p0, p1):
	print(p0)
	print(p1)
	dx = p1[0] - p0[0]
	dy = p1[1] - p0[1]
	dz = p1[2] - p0[2]

	a = dx * dy
	b = dy * p0[0] + dx * p0[1] - dz
	c = p0[0] * p0[1] - p0[2]
	t0 = (-b + math.sqrt((b**2) - (4 * a * c))) / (2 * a)
	t1 = (-b - math.sqrt((b**2) - (4 * a * c))) / (2 * a)

	sp0 = (p0[0] + dx * t0, p0[1] + dy * t0, p0[2] + dz * t0)
	sp1 = (p0[0] + dx * t1, p0[1] + dy * t1, p0[2] + dz * t1)

	#print(sp0)
	#print(sp0[0]*sp0[1]/sp0[2])
	#print(sp1)
	#print(sp1[0]*sp1[1]/sp1[2])

	if sp0[0] >= 0 and sp0[1] > 0 and sp0[2] > 0:
		return sp0
	else:
		return sp1