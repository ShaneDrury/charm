import sys
import os
import pickle
import argparse
import shlex
import pylab
import numpy as np
from pyon.IO import folderIO, get_fit_range
from pyon.Fitting.folder_fit import Meson
from pyon.Fitting import extrapolation
from pyon.Measurements import error_reduce
from pyon import glob_consts

folder = '/temp/srd1g10/results/24c/mesons/0.005_0.005/'
folder_list = [folder+"/pickled.dispersion/p"+str(i)+"/" for i in range(0,5)]
m = []
m_err= []
jl = [] # Jackknife list of masses

for f in folder_list:
    mes = Meson(f)
    out = mes.get_fit()
    jl.append(mes.get_jackknife_lists())
    m.append(out[1])
    m_err.append(out[2])

jl = np.array(jl)
m = np.array(m)
m_err = np.array(m_err)
m_2 = m*m
jl_2 = jl*jl
meas2 = lambda cen, jack: error_reduce.jackknife(cen, jack) # Get jackknife error for fit
m_2_err = map(meas2, m_2, jl_2)

#m_2_err = 2 * m * m_err # This line may be rubbish: it's a good approximation though

print m_2, m_2_err

L = 24
a_inv = 1.73 # inverse lattice spacing in GeV: Not used
p = [0,1,2,3,4]
p_2 = [(2*np.pi/L)**2 * x for x in p]
#sin_p_2 = [a_inv**2 * np.sin(pp / (a_inv)**2) for pp in p_2] # Makes very little difference
#theory = [m_2[0] + x for x in p_2]
theory = [1.0 for x in p_2]

jlT = np.transpose(jl_2)
meas1 = lambda data: extrapolation.dispersion_get_params1(data, p_2, m_2[0], m_2_err)
meas2 = lambda data: extrapolation.dispersion_get_params2(data, p_2, m_2_err)
jack_c1 = map(meas1, jlT)
out2=map(meas2, jlT)
jack_c2 = []
jack_m2 = []
for jc, jm in out2:
    jack_c2.append(jc)
    jack_m2.append(jm)
c1 = np.average(jack_c1)
c2 = np.average(jack_c2)
m2 = np.average(jack_m2)

#out = extrapolation.dispersion_get_params(m_2, p_2, m_2_err)
#c = out[0]
error1 = error_reduce.jackknife(c1, jack_c1)
error2 = error_reduce.jackknife(c2, jack_c2)

print "Effective speed of light One parameter:",c1, error1
print "Effective speed of light Two parameter:",c2, error2

#measure = np.sqrt((m_2[1] - m_2[0])/(p_2[1] - p_2[0]))
jl_2 = np.array(jl_2)
measj = np.sqrt((jl_2[1]-jl_2[0])/(p_2[1] - p_2[0]))
meas_central = np.average(measj)
meas_err = error_reduce.jackknife(meas_central, measj)
print "Measure", meas_central, meas_err
m_2_fit = [m_2[0]*(c1**2)**2 + pp*c1**2 for pp in p_2]
#print m_2_fit
m_2_scaled = m_2 / m_2_fit
pylab.errorbar(p_2, m_2_scaled, yerr=m_2_err)

pylab.xlabel('p^2')
pylab.xlim(-1, 2)
pylab.ylabel('E^2')
pylab.plot(p_2, theory)
#pylab.plot(p_2, m_2_fit)
#pylab.plot(p_2, theory_2)
pylab.show()
