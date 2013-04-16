from pyon.Classes.hadron import PseudoscalarMeson, Baryon
from pyon.Classes import lattice
from pyon.Error import error_reduce
from pyon.IO import prettify
import numpy as np

FIT=True

my_lattice = lattice.Lattice24c()
d = '/home/srd1g10/charm/data/24c/mesons/0.005_0.005/'
folders = (d+'pickled.g15.g15.p16/', d+'pickled.g7.g7.p16/', d+'pickled.g7.g15.p16/')

mes = PseudoscalarMeson.load_from_folder(folders, fit_range=(8, 31),
                                         name="(0.005, 0.005)",
                                         lattice=my_lattice,
                                         fit_type='simultaneous',
                                         mass_guess=0.188,
                                         covariant=True,
                                         correlated=False, frozen_error=True,
                                         num_bins=2, verbose=False)
if FIT:
    print "Meson"
    mes.fit()
    mjl = mes.get_jackknife_lists()
    print mes.get_fit_params()
    print mes.get_fit_params_latex()
else:
    pass
    #mes.plot_graph()

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
if FIT:
    print "Baryon"
    bar.fit()
    bjl = bar.get_jackknife_lists()
    print bar.get_fit_params()
    print bar.get_fit_params_latex()
    #bar.plot_graph()
else:
    bar.plot_graph()


ratiojl = mjl/bjl
central = np.average(ratiojl, axis=0)
error = error_reduce.jackknife(central, ratiojl)
print "m_pi / m_omega"
print central, error
print mes.name + ",", bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"
