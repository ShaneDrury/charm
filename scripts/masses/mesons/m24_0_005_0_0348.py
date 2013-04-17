from pyon.Classes.hadron import PseudoscalarMeson
from pyon.Classes import lattice
#from pyon.Error import error_reduce
#import numpy as np
FIT=True
my_lattice = lattice.Lattice24c()
d = '/export/scratch/srd1g10/results/24c/mesons/0.005_0.0348/'
folders = (d+'pickled.g15.g15.p16/', d+'pickled.g7.g7.p16/', d+'pickled.g7.g15.p16/')

mes = PseudoscalarMeson.load_from_folder(folders, fit_range=(8, 31),
                                         name="(0.005, 0.0348)",
                                         lattice=my_lattice,
                                         fit_type='simultaneous',
                                         mass_guess=0.3,
                                         covariant=True,
                                         correlated=False, frozen_error=True,
                                         num_bins=2, verbose=False)

def get_mass():
    mes.fit()
    return mes.get_jackknife_lists()

if __name__== "__main__":
    if FIT:
        mes.fit()
        print mes.get_fit_params()
        print mes.get_fit_params_latex()
    else:
        mes.plot_graph()
