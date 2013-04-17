"""
Do the extrapolation in m_l
"""
from pyon.Classes.hadron import PseudoscalarMeson, Baryon
from pyon.Classes import lattice
import numpy as np
#from pyon.Resampling import jackknife
from pyon.Measurements import error_reduce
from pyon.Error.error_reduce import extend
from pyon import glob_consts
from pyon.Fitting import extrapolation
from pyon.IO import prettify
from charm.scripts.masses.ratios import komega32_0_006_0_0273_0_0273 as k32
from charm.scripts.masses.mesons import m24_0_005_0_005, m24_0_01_0_01, m24_0_005_0_0348, m24_0_01_0_0348
from charm.scripts.masses.baryons import b24_0_0348
import pylab

mpimomega32 = 0.1960 # Our target

m24jl_005 = m24_0_005_0_005.get_mass()
m24jl_01 = m24_0_01_0_01.get_mass()
b24jl_0348 = b24_0_0348.get_mass()
mpimomega24j = np.array([m24jl_005, m24jl_01])
mpimomega24j = mpimomega24j / b24jl_0348
mpimomega24 = np.average(mpimomega24j, axis=1)

x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_pi_m_omega_get_params(data, x) # Get fit params
meas2 = lambda (a,b): (extrapolation.m_pi_m_omega_get_m(mpimomega32, a, b) - glob_consts.mres24) # Invert relation to find extrapolated mass

params = map(meas1, np.transpose(mpimomega24j))
params_central = np.average(params, axis=0)

jmasses = map(meas2, params)
central = np.average(jmasses, axis=0)
error = error_reduce.jackknife(central, jmasses)
m_l = central
m_l_err = error
print "Extrapolated m_l", central, error
print  "$m_l=", prettify.bracket_error(central, error)+"$"

def ratio_functional(m, A, B):
    return A * np.sqrt(m) / (1.0 + B * m)
rat_m = lambda m: ratio_functional(m, params_central[0], params_central[1])

ext_ratio = rat_m(central + glob_consts.mres24)
x_range = np.arange(0.005, 0.01, 1e-5)
curve = [rat_m(x + glob_consts.mres24) for x in x_range]
pylab.scatter([0.005, 0.01], mpimomega24)
pylab.plot(x_range, curve)
pylab.plot([central], [ext_ratio], 'x', color='red')
#pylab.show()

# Now do same for LH
m24jlLH1 = m24_0_005_0_0348.get_mass()
m24jlLH2 = m24_0_01_0_0348.get_mass()
mkmomega24j = np.array([m24jlLH1, m24jlLH2]) / b24jl_0348
mkmomega24 = np.average(mkmomega24j, axis=1)
x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_k_m_omega_get_params2(data, x) # Get fit params
meas2 = lambda m,(a,b): extrapolation.m_k_m_omega_get_r2(m,a,b)

params = map(meas1, np.transpose(mkmomega24j))
jratios = map(meas2, np.array(jmasses) + glob_consts.mres24, params)

central = np.average(jratios, axis=0)
error = error_reduce.jackknife(central, jratios)
print "m_K/m_omega @ m_l", central, error
print "("+prettify.bracket_error(m_l, m_l_err) +", "+ prettify.bracket_error(m_l, m_l_err)+ ")" + ",", b24_0_0348.bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"


print "Ratio"
ratiojl = k32.get_ratio()
central = np.average(ratiojl, axis=0)
error = error_reduce.jackknife(central, ratiojl)
print "m_pi / m_omega"
print central, error
print k32.m32.mes.name + ",", k32.b32.bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"

def S(a,b):
    return a/b
R_24, R_32 = extend(jratios, ratiojl)
R_24 = np.array(R_24)
R_32 = np.array(R_32)
Sjl = S(R_24, R_32)
S_central = np.average(Sjl, axis=0)
S_err = error_reduce.jackknife(S_central, Sjl)
print S_central, S_err
print "Ratio", prettify.bracket_error(S_central, S_err)

