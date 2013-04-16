from pyon.Classes.hadron import PseudoscalarMeson
from pyon.Classes import lattice
#from pyon.Error import error_reduce
#import numpy as np
FIT = True
my_lattice = lattice.Lattice24c()
d = '/home/srd1g10/charm/data/24c/mesons/0.01_0.01/'
folders = (d+'pickled.g15.g15.p16/', d+'pickled.g7.g7.p16/', d+'pickled.g7.g15.p16/')

mes = PseudoscalarMeson.load_from_folder(folders, fit_range=(9, 31),
                                         name="(0.01, 0.01)",
                                         lattice=my_lattice,
                                         fit_type='simultaneous',
                                         mass_guess=0.24,
                                         covariant=True,
                                         correlated=False, frozen_error=True,
                                         num_bins=2, verbose=False)


if FIT:
    mes.fit()
    print mes.get_fit_params()
    print mes.get_fit_params_latex()
mes.plot_graph()
