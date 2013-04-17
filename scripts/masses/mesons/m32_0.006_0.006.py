from pyon.Classes.hadron import PseudoscalarMeson
from pyon.Classes import lattice
#from pyon.Error import error_reduce
#import numpy as np
FIT=True
my_lattice = lattice.Lattice32c()
d = '/export/scratch/srd1g10/results/32c/mesons/0.006_0.006/'
folders = (d+'pickled.g15.g15.p16/', d+'pickled.g7.g7.p16/', d+'pickled.g7.g15.p16/')

mes = PseudoscalarMeson.load_from_folder(folders, fit_range=(9, 31),
                                         name="(0.006, 0.006)",
                                         lattice=my_lattice,
                                         fit_type='simultaneous',
                                         mass_guess=0.188,
                                         covariant=True,
                                         correlated=False, frozen_error=True,
                                         num_bins=2, verbose=False)


if FIT:
    mes.fit()
    print mes.get_fit_params()
    print mes.get_fit_params_latex()
mes.plot_graph()