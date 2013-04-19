import pickle
import numpy as np
from pyon import glob_consts
from pyon.Error.error_reduce import mean_and_error
from pyon.Fitting import extrapolation
from charm.scripts.masses.ratios import komega32_0_006_0_05_0_05 as k32_05

k32_05jl = k32_05.get_ratio()
k32_05, err = mean_and_error(k32_05jl)
#print mean_and_error(k24_0348jl)

with open("/home/srd1g10/charm/data/jl/mkmomega24_0_0348mljl", "r") as g:
    mkmomega24_0_0348mljl = pickle.load(g)  # Has m_s = 0.0348

with open("/home/srd1g10/charm/data/jl/mkmomega24_0_04mljl", "r") as g:
    mkmomega24_0_04mljl = pickle.load(g)  # Has m_s = 0.04

mkmomega24j = [mkmomega24_0_0348mljl, mkmomega24_0_04mljl]
print np.average(mkmomega24j, axis=1)
#central, error = mean_and_error(mkmomega24_0_04mljl)
#print "m_K/m_omega @ m_l", central, error

x = [0.0348+glob_consts.mres24, 0.04+glob_consts.mres24]
meas1 = lambda data: extrapolation.linear_get_params(data, x) # Get fit params
meas2 = lambda (a,b): (extrapolation.linear_get_m(k32_05, a, b) - glob_consts.mres24) # Invert relation to find extrapolated mass

params = map(meas1, np.transpose(mkmomega24j))
params_central = np.average(params, axis=0)
#A, B = params_central
#print A * (0.04 + glob_consts.mres24) + B

mcjl = map(meas2, params)  # m_l jackknife lists
print mean_and_error(mcjl)
