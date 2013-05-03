import pickle
import numpy as np
import pylab
from pyon import glob_consts
from pyon.Error.error_reduce import mean_and_error
from pyon.IO import prettify
from pyon.Fitting import extrapolation
from charm.scripts.masses.ratios import komega32_0_006_0_08_0_08 as k32r
import scipy.interpolate as sp
import minuit

charm_masses = [0.0348, 0.04, 0.0472, 0.055, 0.0613, 0.07, 0.1, 0.12, 0.123, 0.132]
files = [str(m).replace(".", "_") for m in charm_masses]
suf = "mljl"


jldir = "/home/srd1g10/charm/data/jl/mkmomega24_"
jlists = []
for m in files:
    with open(jldir + m + suf, "r") as g:
        jlists.append(pickle.load(g))

ratios = np.average(jlists, axis=1) # List of points on graph


k32jl = k32r.get_ratio()
k32, err = mean_and_error(k32jl)
x = np.array([m + glob_consts.mres24 for m in charm_masses])

if k32 > min(ratios) and k32 < max(ratios):
    #print k32
    # Interpolate
    fc = sp.interp1d(x, ratios, kind='cubic', fill_value=np.nan)

    def f(x):
        return (k32 - fc(x))**2
    m = minuit.Minuit(f, x=0.06)
    m.migrad()
    mass = m.values['x'] - glob_consts.mres24
    xnew = np.arange(x[0], x[-1], 1e-4)
    print "Interpolated mass:", mass
    pylab.plot(x, ratios, 'o', xnew, fc(xnew))
    pylab.plot([mass + glob_consts.mres24], [k32], 'x', color='red')
    pylab.show()


#  Note: the linear extrapolation is poor. Use interpolation 
#  or linear extrapolation for very very small intervals.

#meas1 = lambda data: extrapolation.linear_get_params(data, x) # Get fit params
#meas2 = lambda (a,b): (extrapolation.linear_get_m(k32_05, a, b) - glob_consts.mres24)# Invert relation to find extrapolated mass
#params = map(meas1, np.transpose(jlists))
#params_central = np.average(params, axis=0)
#A, B = params_central
#y = A * x + B
#pylab.plot(x,y)
#mcjl = map(meas2, params)  # m_l jackknife lists
#central, error = mean_and_error(mcjl)
#central = central - glob_consts.mres24
#print prettify.bracket_error(central, error)
