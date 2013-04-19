"""
Do the extrapolation in m_l
"""
import numpy as np
from pyon.Error.error_reduce import pad, mean_and_error
from pyon import glob_consts
from pyon.Fitting import extrapolation
from pyon.IO import prettify
from charm.scripts.masses.ratios import komega32_0_006_0_0273_0_0273 as k32
from charm.scripts.masses.ratios import piomega32_0_006_0_006_0_0273 as p32
from charm.scripts.masses.mesons import m24_0_005_0_005, m24_0_01_0_01, m24_0_005_0_0348, m24_0_01_0_0348
from charm.scripts.masses.baryons import b24_0_0348
import pylab
import pickle

#mpimomega32 = 0.1960  # Our target
mpimomega32jl = p32.get_ratio()
mpimomega32, mpimomega32_err = mean_and_error(mpimomega32jl)
print "m_pi/m_omega 32c", prettify.bracket_error(mpimomega32, mpimomega32_err)

b24jl_0348 = b24_0_0348.get_mass()
mpimomega24j = np.array([m24_0_005_0_005.get_mass(), m24_0_01_0_01.get_mass()]) / b24jl_0348  # Get ratio
mpimomega24 = np.average(mpimomega24j, axis=1)

x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_pi_m_omega_get_params(data, x) # Get fit params
meas2 = lambda (a,b): (extrapolation.m_pi_m_omega_get_m(mpimomega32, a, b) - glob_consts.mres24) # Invert relation to find extrapolated mass

params = map(meas1, np.transpose(mpimomega24j))
params_central = np.average(params, axis=0)

jmasses = map(meas2, params)  # m_l jackknife lists

with open("/home/srd1g10/charm/data/jl/mljl", 'w') as g:
    pickle.dump(jmasses, g)
central, error = mean_and_error(jmasses)
m_l = central
m_l_err = error
print "Extrapolated m_l", central, error
print  "$m_l=", prettify.bracket_error(central, error)+"$"

#----------------------------------------------------------------
# Check if m_pi / m_omega @ m_l is same

def ratio_fn(m, A, B):
    return A * np.sqrt(m) / (1.0 + B * m)

#rat_m = lambda m: ratio_fu(m, params_central[0], params_central[1])
r_ratio_jl = [ratio_fn(jml + glob_consts.mres24, pp[0], pp[1]) for jml, pp in zip(jmasses, params)]
#r_ratio, r_ratio_err = mean_and_error(r_ratio_jl)
#ext_ratio = rat_m(central + glob_consts.mres24)

R_24, R_32 = pad(r_ratio_jl, mpimomega32jl)
R_24 = np.array(R_24)
R_32 = np.array(R_32)
Rjl = R_24 / R_32
R_central, R_err = mean_and_error(Rjl)

print R_central, R_err
print "Ratio S", prettify.bracket_error(R_central, R_err)  # this error displays wrong

#----------------------------------------------------------------
# Now do same for LH
m24jlLH1 = m24_0_005_0_0348.get_mass()
m24jlLH2 = m24_0_01_0_0348.get_mass()
mkmomega24j = np.array([m24jlLH1, m24jlLH2]) / b24jl_0348
mkmomega24 = np.average(mkmomega24j, axis=1)
print mkmomega24
x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_k_m_omega_get_params2(data, x) # Get fit params
meas2 = lambda m,(a,b): extrapolation.m_k_m_omega_get_r2(m,a,b)

params = map(meas1, np.transpose(mkmomega24j))
jratios = map(meas2, np.array(jmasses) + glob_consts.mres24, params) # m_k_m_omega at m_l
central, error = mean_and_error(jratios)
print "m_K/m_omega @ m_l", central, error
print "("+prettify.bracket_error(m_l, m_l_err) +", "+ prettify.bracket_error(m_l, m_l_err)+ ")" + ",", b24_0_0348.bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"
with open("/home/srd1g10/charm/data/jl/mkmomega24mljl", 'w') as g:
    pickle.dump(jratios, g)

#----------------------------------------------------------------
print "Ratio"
ratiojl = k32.get_ratio()
central, error = mean_and_error(ratiojl)
print "m_pi / m_omega"
print central, error
print k32.m32.mes.name + ",", k32.b32.bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"

R_24, R_32 = pad(jratios, ratiojl)
R_24 = np.array(R_24)
R_32 = np.array(R_32)
Sjl = R_24 / R_32
S_central, S_err = mean_and_error(Sjl)

print S_central, S_err
print "Ratio S", prettify.bracket_error(S_central, S_err)

