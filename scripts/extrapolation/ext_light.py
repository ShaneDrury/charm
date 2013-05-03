"""
Do the extrapolation in m_l by loading in the jackknife lists
"""
import numpy as np
from pyon.Error.error_reduce import pad, mean_and_error
from pyon import glob_consts
from pyon.Fitting import extrapolation
from pyon.IO import prettify
from charm.scripts.masses.ratios import komega32_0_006_0_05_0_05 as k32
from charm.scripts.masses.mesons import m24_0_005_0_0613 as m24_1
from charm.scripts.masses.mesons import m24_0_01_0_0613 as m24_2
from charm.scripts.masses.baryons import b24_0_0613 as b24
import pickle
to_save = "mkmomega24_0_0613mljl"

with open("/home/srd1g10/charm/data/jl/mljl", "r") as g:
    mljl = pickle.load(g)

b24jl = b24.get_mass()
m24jlLH1 = m24_1.get_mass()
m24jlLH2 = m24_2.get_mass()
#b24jl, m24jlLH1 = pad(b24jl, m24jlLH1)
mkmomega24j = np.array([m24jlLH1, m24jlLH2]) / b24jl
mkmomega24 = np.average(mkmomega24j, axis=1)
print mkmomega24
x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_k_m_omega_get_params2(data, x) # Get fit params
meas2 = lambda m,(a,b): extrapolation.m_k_m_omega_get_r2(m,a,b)

params = map(meas1, np.transpose(mkmomega24j))
jratios = map(meas2, np.array(mljl) + glob_consts.mres24, params) # m_k_m_omega at m_l
central, error = mean_and_error(jratios)
print central, error
print "m_K/m_omega @ m_l", prettify.bracket_error(central, error)

ratiojl = k32.get_ratio()
R_24, R_32 = pad(jratios, ratiojl)
R_24 = np.array(R_24)
R_32 = np.array(R_32)
Sjl = R_24 / R_32
S_central, S_err = mean_and_error(Sjl)

print S_central, S_err # m_k / m_omega ratio
print "Ratio S", prettify.bracket_error(S_central, S_err)

#with open("/home/srd1g10/charm/data/jl/" + to_save, 'w') as g:
#    pickle.dump(jratios, g)

