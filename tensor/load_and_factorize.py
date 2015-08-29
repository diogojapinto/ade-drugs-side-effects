import scipy.io as sio
import numpy as np
from hosvd import hosvd, reconstruct_tensor
from utils import save_file, read_file, cosine_distance

def load(file_name,mat_name='x'):
    return sio.loadmat(file_name)[mat_name]

def factorize(T):
    return hosvd(T)

def load_and_factorize(file_name,mat_name='x'):
    T = load(file_name,mat_name)
    S,U = factorize(T)
    return T,S,U

def diff_tensor(T,S,U):
    T_hat = reconstruct_tensor(S,U)
    return T-T_hat

def find_interesting_indexes(T,S,U,diff_threshold):
    diff = diff_tensor(T,S,U)

    return diff > diff_threshold

def predict_adr(T,U,input_adr):
    projected_adr = np.dot(input_adr,U[1])
    (drugs,adrs,people) = T.shape
    output_adr = np.zeros(adrs)

    for i in range(adrs):
        output_adr[i] = cosine_distance(projected_adr,(U[1])[i,:])

    return output_adr

def factorize_and_save(filename,mat_name='x'):
    T,S,U = load_and_factorize(filename,mat_name)

    save_file('S_'+filename,S)
    save_file('U_'+filename,U)

    return T,S,U

def load_saved_files(filename,mat_name='x'):
    T = load(filename,mat_name)
    S = read_file('S_'+filename)
    U = read_file('U_'+filename)

    return T,S,U

if __name__ == '__main__':
    T,S,U = load_saved_files('faers')

    indexes = find_interesting_indexes(T,S,U,1)
    input_adr = T[0,:,0]
    print(input_adr)
    print(predict_adr(T,U,input_adr))
