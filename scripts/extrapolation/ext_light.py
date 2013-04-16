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
import pylab

my_lattice = lattice.Lattice24c()
mfolders = ('/export/scratch/srd1g10/results/24c/mesons/0.005_0.005/','/export/scratch/srd1g10/results/24c/mesons/0.01_0.01/')
bfolder = '/export/scratch/srd1g10/results/24c/baryons/0.005_0.005_0.0348/'
mpimomega32 = 0.1960
mpimomega24 = []
mpimomega24j = []
bfolder='/export/scratch/srd1g10/results/24c/baryons/0.005_0.005_0.0348/'
bfolders = (bfolder+'pickled.b14.p16/', bfolder+'pickled.b15.p16/', bfolder+'pickled.b16.p16/')
bar = Baryon.load_from_folder(bfolders, fit_range=(9, 17),
                              name="$0.0348^3$",
                              lattice=my_lattice,
                              fit_type='individual',
                              average_over_folders=True,
                              mass_guess=1.0,
                              covariant=True,
                              correlated=False, frozen_error=True,
                              num_bins=2, verbose=False)
#bar.plot_graph()
if bar.fit():
    #print bar.get_fit_params()
    print bar.get_fit_params_latex()
    bjl=bar.get_jackknife_lists()


names = ["(0.005, 0.005)", "(0.01, 0.01)"]
fit_ranges = [(8, 31), (9, 31)]
for mfolder, name, fit_range in zip(mfolders, names, fit_ranges): # Get m_pi/m_omega for both light masses
    gf = (mfolder+'pickled.g15.g15.p16/', mfolder+'pickled.g7.g7.p16/', mfolder+'pickled.g7.g15.p16/')

    mes = PseudoscalarMeson.load_from_folder(gf, fit_range=fit_range,
                                             name=name,
                                             lattice=my_lattice,
                                             fit_type='simultaneous',
                                             covariant=True,
                                             correlated=False, frozen_error=True,
                                             num_bins=2, verbose=False)
    if mes.fit():
        #print mes.get_fit_params()
        print mes.get_fit_params_latex()
        mjl=mes.get_jackknife_lists()

    jack_lists = mjl/bjl
    central = np.average(jack_lists, axis=0)
    error = error_reduce.jackknife(central, jack_lists)
    mpimomega24j.append(jack_lists)
    mpimomega24.append(central)
    
    #print "m_pi/m_omega", central, error
    print mes.name + ",", bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"

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

names = ["(0.005, 0.0348)", "(0.01, 0.0348)"]
fit_ranges = [(8, 31), (8, 31)]
mkmomega24 = []
mkmomega24j = []

mfolders = ('/export/scratch/srd1g10/results/24c/mesons/0.005_0.0348/','/export/scratch/srd1g10/results/24c/mesons/0.01_0.0348/')

for mfolder, name, fit_range in zip(mfolders, names, fit_ranges): # Get m_K/m_omega for both light masses
    gf = (mfolder+'pickled.g15.g15.p16/', mfolder+'pickled.g7.g7.p16/', mfolder+'pickled.g7.g15.p16/')

    mes = PseudoscalarMeson.load_from_folder(gf, fit_range=fit_range,
                                             name=name,
                                             lattice=my_lattice,
                                             fit_type='simultaneous',
                                             covariant=True,
                                             correlated=False, frozen_error=True,
                                             num_bins=2, verbose=False)
    if mes.fit():
        #print mes.get_fit_params()
        print mes.get_fit_params_latex()
        mjl=mes.get_jackknife_lists()

    jack_lists = mjl/bjl
    central = np.average(jack_lists, axis=0)
    error = error_reduce.jackknife(central, jack_lists)
    mkmomega24j.append(jack_lists)
    mkmomega24.append(central)

    print mes.name + ",", bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"

x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_k_m_omega_get_params2(data, x) # Get fit params
meas2 = lambda m,(a,b): extrapolation.m_k_m_omega_get_r2(m,a,b)

params = map(meas1, np.transpose(mkmomega24j))
jratios = map(meas2, np.array(jmasses) + glob_consts.mres24, params)

central = np.average(jratios, axis=0)
error = error_reduce.jackknife(central, jratios)
print "m_K/m_omega @ m_l", central, error
print "("+prettify.bracket_error(m_l, m_l_err) +", "+ prettify.bracket_error(m_l, m_l_err)+ ")" + ",", bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"


print "Ratio"
my_lattice = lattice.Lattice32c()
d = '/export/scratch/srd1g10/results/32c/mesons/0.006_0.0273/'
folders = (d+'pickled.g15.g15.p16/', d+'pickled.g7.g7.p16/', d+'pickled.g7.g15.p16/')

mes = PseudoscalarMeson.load_from_folder(folders, fit_range=(10, 31),
                                         name="(0.006, 0.0273)",
                                         lattice=my_lattice,
                                         fit_type='simultaneous',
                                         mass_guess=0.24,
                                         covariant=True,
                                         correlated=False, frozen_error=True,
                                         num_bins=2, verbose=False)
print "Meson"
mes.fit()
mjl = mes.get_jackknife_lists()
print mes.get_fit_params_latex()

bfolder='/export/scratch/srd1g10/results/32c/baryons/0.006_0.006_0.0273/'
bfolders = (bfolder+'pickled.b14.p16/', bfolder+'pickled.b15.p16/', bfolder+'pickled.b16.p16/')
bar = Baryon.load_from_folder(bfolders, fit_range=(11, 23),
                              name="$0.0273^3$",
                              lattice=my_lattice,
                              fit_type='individual',
                              average_over_folders=True,
                              mass_guess=0.77,
                              covariant=True,
                              correlated=False, frozen_error=True,
                              num_bins=2, verbose=False)
print "Baryon"
bar.fit()
bjl = bar.get_jackknife_lists()
print bar.get_fit_params_latex()

ratiojl = mjl/bjl
central = np.average(ratiojl, axis=0)
error = error_reduce.jackknife(central, ratiojl)
print "m_pi / m_omega"
print central, error
print mes.name + ",", bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"

def S(a,b):
    return a/b
R_24, R_32 = extend(jratios, ratiojl)
R_24 = np.array(R_24)
R_32 = np.array(R_32)
Sjl = S(R_24, R_32)
S_central = np.average(Sjl, axis=0)
S_err = error_reduce.jackknife(S_central, Sjl)
print S_central, S_err
print mes.name + ",", bar.name, "&", prettify.bracket_error(S_central, S_err), "\\\ \hline"

