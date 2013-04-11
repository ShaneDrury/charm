"""
Do the extrapolation in m_l, find m_k/m_omega at this m_l
"""
from pyon.Classes.hadron import PseudoscalarMeson, Baryon
from pyon.Classes import lattice
import numpy as np
#from pyon.Resampling import jackknife
from pyon.Measurements import error_reduce
from pyon import glob_consts
from pyon.Fitting import extrapolation

my_lattice = lattice.Lattice24c()
mfolders = ('/export/scratch/srd1g10/results/24c/mesons/0.005_0.005/','/export/scratch/srd1g10/results/24c/mesons/0.01_0.01/')
bfolder = '/export/scratch/srd1g10/results/24c/baryons/0.005_0.005_0.0348/'
#mpimomega32 = 0.1982
#mpimomega32 = 0.1972
mpimomega24 = []
mpimomega24j = []
bfolders = (bfolder+'pickled.b14.p16/', bfolder+'pickled.b15.p16/', bfolder+'pickled.b16.p16/')
bar = Baryon.load_from_folder(bfolders, fit_range=(9, 16),
                              name="baryon",
                              lattice=my_lattice,
                              fit_type='individual',
                              average_over_folders=True,
                              covariant=True,
                              correlated=False, frozen_error=True,
                              num_bins=2, verbose=False)
bar.plot_graph()
if bar.fit():
    print bar.get_fit_params()
    bjl=bar.get_jackknife_lists()
for mfolder in mfolders: # Get m_pi/m_omega for both light masses
    mfolders = (mfolder+'pickled.g15.g15.p16/', mfolder+'pickled.g7.g7.p16/', mfolder+'pickled.g7.g15.p16/')

    mes = PseudoscalarMeson.load_from_folder(mfolders, fit_range=(8, 31),
                                             name="meson",
                                             lattice=my_lattice,
                                             fit_type='simultaneous',
                                             covariant=True,
                                             correlated=False, frozen_error=True,
                                             num_bins=2, verbose=False)
    if mes.fit():
        print mes.get_fit_params()
        mjl=mes.get_jackknife_lists()

    jack_lists = mjl/bjl
    central = np.average(jack_lists, axis=0)
    error = error_reduce.jackknife(central, jack_lists)
    mpimomega24j.append(jack_lists)
    mpimomega24.append(central)
    
    print mfolder, "m_pi/m_omega", central, error

x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
meas1 = lambda data: extrapolation.m_pi_m_omega_get_params(data, x) # Get fit params
meas2 = lambda (a,b): (extrapolation.m_pi_m_omega_get_m(mpimomega32, a, b) - glob_consts.mres24) # Invert relation to find extrapolated mass

params = map(meas1, np.transpose(mpimomega24j))
jmasses = map(meas2, params)
central = np.average(jmasses, axis=0)
error = error_reduce.jackknife(central, jmasses)
print "Extrapolated m_l", central, error

# # Now do same for LH
# mfolders = ('/export/scratch/srd1g10/results/24c/mesons/0.005_0.07/','/export/scratch/srd1g10/results/24c/mesons/0.01_0.07/')
# bfolder = '/export/scratch/srd1g10/results/24c/baryons/0.005_0.005_0.07/'
# mkmomega24 = []
# mkmomega24j = []
# for mfolder in mfolders: # Get m_pi/m_omega for both light masses
#     mes = Meson(mfolder)
#     bar = Baryon(bfolder)
#     mjl = mes.get_jackknife_lists()[0]
#     bjl = bar.get_jackknife_lists()
#     print len(mjl), len(bjl)
#     jack_lists = mjl/bjl
#     central = np.average(jack_lists, axis=0)
#     error = error_reduce.jackknife(central, jack_lists)

#     mk24 = np.average(mjl, axis=0)
#     mk24_err = error_reduce.jackknife(mk24, mjl)
#     momega24 = np.average(bjl, axis=0)
#     momega24_err = error_reduce.jackknife(momega24, bjl)

#     mkmomega24j.append(jack_lists)
#     mkmomega24.append(central)
#     print mfolder, "m_K/m_omega", central, error

# x = [0.005+glob_consts.mres24, 0.01+glob_consts.mres24]
# meas1 = lambda data: extrapolation.m_k_m_omega_get_params2(data, x) # Get fit params
# #meas2 = lambda (a,b): (extrapolation.m_pi_m_omega_get_m(mkmomega32, a, b) - glob_consts.mres24) # Invert relation to find extrapolated mass
# meas2 = lambda m,(a,b): extrapolation.m_k_m_omega_get_r2(m,a,b)

# params = map(meas1, np.transpose(mkmomega24j))
# #print np.average(params, axis=0), np.sqrt(np.std(params, axis=0))
# jratios = map(meas2, np.array(jmasses) + glob_consts.mres24, params)
# #print jratios
# #jk24_extrapolated =  np.array(bjl)*np.array(jratios)

# #mk24_extrapolated = np.average(jk24_extrapolated, axis=0)
# #mk24_extrapolated_err = error_reduce.jackknife(mk24_extrapolated, jk24_extrapolated)
# central = np.average(jratios, axis=0)
# error = error_reduce.jackknife(central, jratios)
# print "m_K/m_omega @ m_l", central, error
