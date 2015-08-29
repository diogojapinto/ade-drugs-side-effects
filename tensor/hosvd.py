import numpy as np
from sktensor import dtensor,sptensor
from utils import reduce_rank


def _build_sparse_tensor(T):
	subs = np.nonzero(T)
	vals = T[subs]

	print(subs)
	print(vals)

	return sptensor(subs,vals)

def hosvd(T,sparse=False):
	# Sparse not working due to the function np.linalg.svd(Ai)

	if sparse:
		T,S = _build_sparse_tensor(T),_build_sparse_tensor(T)
	else:
		T = dtensor(T)
		S = T.copy()

	U = []

	for i in range(T.ndim):
		Ai = T.unfold(i)
		Ui, Si, _ = np.linalg.svd(Ai)

		ri = reduce_rank(Si)

		Wi = Ui[:,0:ri+1]
		U.append(Wi)

		S = S.ttm(np.transpose(Wi),i)

	return S, U

def reconstruct_tensor(S,U):

	T_hat = S.copy()

	for i in range(len(U)):
		T_hat = T_hat.ttm(U[i],i)

	return T_hat

if __name__ == "__main__":

	# user, query, page
	Toy = np.zeros((4,4,4))
	Toy[0,0,0] = 1

	Toy[1,0,0] = 1
	Toy[1,1,1] = 1
	Toy[1,2,2] = 1

	Toy[2,2,3] = 1
	Toy[2,3,3] = 1

	Toy[3,3,3] = 1

	#Toy = dtensor(Toy)

	S,U = hosvd(Toy)
	Toy_hat = reconstruct_tensor(S,U)
	print(Toy_hat)
