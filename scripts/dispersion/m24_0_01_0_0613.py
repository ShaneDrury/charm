from pyon.Classes.hadron import PseudoscalarMeson
from pyon.Classes import lattice
import Gnuplot
from pyon.Error import error_reduce
import numpy as np
from pyon.IO import prettify
FIT=True
my_lattice = lattice.Lattice24c()
d = '/temp/srd1g10/results/24c/mesons/0.01_0.0613/pickled.dispersion/'
folders = [d+'p0/', d+'p1/']
fit_ranges = [(8, 31), (8, 27)]
guesses = [0.39, 0.49]
names = ['p0', 'p1']
jl = []
for folder, fit_range, guess, name in zip(folders, fit_ranges, guesses, names):
    mes = PseudoscalarMeson.load_from_folder(folder, fit_range=fit_range,
                                             name="(0.01, 0.0613) " + name,
                                             lattice=my_lattice,
                                             fit_type='individual',
                                             mass_guess=guess,
                                             covariant=True,
                                             correlated=False, frozen_error=True,
                                             num_bins=2, verbose=False)
    #mes.plot_graph()
    mes.fit()
    jl.append(mes.get_jackknife_lists())

jl = np.array(jl)

def get_c():

    jl_2 = jl * jl
    masses = np.average(jl, axis=1) # central masses
    m_2 = masses * masses
    L = 24
    c = (m_2[1] - m_2[0])/ ( 2 * np.pi / L) ** 2 # central
    cjl = (jl_2[1] - jl_2[0])/ ( 2 * np.pi / L) ** 2 # jackknife
    cc, cce = error_reduce.mean_and_error(cjl);return cc, cce, masses[0]

if __name__== "__main__":
    if FIT:
        jl = np.array(jl)
        jl_2 = jl * jl
        masses = np.average(jl, axis=1) # central masses
        m_2 = masses * masses
        L = 24
        c = (m_2[1] - m_2[0])/ ( 2 * np.pi / L) ** 2 # central
        cjl = (jl_2[1] - jl_2[0])/ ( 2 * np.pi / L) ** 2 # jackknife
        cm, cerr = error_reduce.mean_and_error(cjl)
        print cm, cerr
        print prettify.bracket_error(cm, cerr)
    else:
        pass

