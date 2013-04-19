"""
Do the extrapolation in m_l by loading in the jackknife lists
"""
import numpy as np
from pyon.Error.error_reduce import pad, mean_and_error
from pyon import glob_consts
from pyon.Fitting import extrapolation
from pyon.IO import prettify
from charm.scripts.masses.mesons import m24_0_005_0_04 as m24_1
from charm.scripts.masses.mesons import m24_0_01_0_04 as m24_2
from charm.scripts.masses.baryons import b24_0_04 as b24
import pickle

with open("/home/srd1g10/charm/data/jl/mljl", "r") as g:
    mljl = pickle.load(g)

b24jl = b24.get_mass()
m24jlLH1 = m24_1.get_mass()
m24jlLH2 = m24_2.get_mass()
mkmomega24j = np.array([m24jlLH1, m24jlLH2]) / b24jl
mkmomega24 = np.average(mkmomega24j, axis=1)
print mkmomega24
x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_k_m_omega_get_params2(data, x) # Get fit params
meas2 = lambda m,(a,b): extrapolation.m_k_m_omega_get_r2(m,a,b)

params = map(meas1, np.transpose(mkmomega24j))
jratios = map(meas2, np.array(mljl) + glob_consts.mres24, params) # m_k_m_omega at m_l
central, error = mean_and_error(jratios)
print "m_K/m_omega @ m_l", central, error

with open("/home/srd1g10/charm/data/jl/mkmomega24_0_04mljl", 'w') as g:
    pickle.dump(jratios, g)

