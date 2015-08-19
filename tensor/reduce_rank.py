
def reduce_rank(S, energy_retain=0.9):
	energy = 0
	r=-1
	for elem in S:
		energy = energy + elem**2
		r = r+1

	cur_energy = energy

	while cur_energy > energy*energy_retain:
		cur_energy = cur_energy - S[r]**2
		r = r-1

	return r