import numpy as np
import numpy.linalg
import pickle

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

def save_file(filename,obj,mode='wb'):
	with open(filename,mode) as f:
		pickle.dump(obj,f)

def read_file(filename,mode='rb'):
	with open(filename,mode) as f:
		obj = pickle.load(f)
	return obj

def cosine_distance(a,b):
	norms = np.linalg.norm(a) * np.linalg.norm(b)
	if  norms == 0:
		return norms

	return np.dot(a,b) / norms
