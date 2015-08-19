import tensor_unfolding as un
import numpy as np
import scipy as sp
from sktensor import dtensor
from reduce_rank import reduce_rank

def hosvd(T):

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

	Toy = dtensor(Toy)
	
	S,U = hosvd(Toy)
	Toy_hat = reconstruct_tensor(S,U)