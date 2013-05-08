from pyon.Classes.hadron import PseudoscalarMeson
from pyon.Classes import lattice
import Gnuplot
#from pyon.Error import error_reduce
import numpy as np
import pylab as pl
FIT=True
my_lattice = lattice.Lattice24c()
d = '/temp/srd1g10/results/24c/mesons/0.005_0.005/pickled.dispersion/'
folders = [d+'p0/', d+'p1/', d+'p2/', d+'p3/', d+'p4/']
fit_ranges = [(8, 31), (8, 31), (8, 31), (8, 31), (8, 31)]
guesses = [0.19, 0.33, 0.44, 0.56, 0.5947266]
names = ['p0', 'p1', 'p2', 'p3', 'p4']
#m = []
#m_err = []
jl = []
for folder, fit_range, guess, name in zip(folders, fit_ranges, guesses, names):
    mes = PseudoscalarMeson.load_from_folder(folder, fit_range=fit_range,
                                             name="(0.005, 0.005) " + name,
                                             lattice=my_lattice,
                                             fit_type='individual',
                                             mass_guess=guess,
                                             covariant=True,
                                             correlated=False, frozen_error=True,
                                             num_bins=2, verbose=False)
    #mes.plot_graph()
    mes.fit()
    #fit_params = mes.get_fit_params_raw()
    #m.append(fit_params['m'])
    #m_err.append(fit_params['m_err'])
    jl.append(mes.get_jackknife_lists())

masses = np.average(jl, axis=1) # masses
m_2 = masses * masses

L = 24
#a_inv = 1.73 # inverse lattice spacing in GeV: Not used
p = [0,1,2,3,4]
p_2 = [(2*np.pi/L)**2 * x for x in p]
c = (m_2[1] - m_2[0])/ ( p_2[1] - p_2[0])
print c
#theory = [1.0 for x in p_2]
scaled = m_2 / (m_2[0] + p_2)

g = Gnuplot.Gnuplot(persist=True)
data = Gnuplot.Data(zip(p_2, m_2))
g.plot(data)


def get_mass():
    mes.fit()
    return mes.get_jackknife_lists()
"""
if __name__== "__main__":
    if FIT:
        mes.fit()
        print mes.get_fit_params()
        print mes.get_fit_params_latex()
    else:
        mes.plot_graph()
"""
