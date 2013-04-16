from pyon.Error.error_reduce import extend
import numpy as np

def S(a,b):
    return a/b
j1 = np.array([0,1,2,3])
j2 = np.array([0,1,2,3,5,8])
extend(S, j1, j2)
