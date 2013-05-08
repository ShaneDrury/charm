from pyon.Classes.hadron import Baryon
from pyon.Classes import lattice

#from pyon.Error import error_reduce
#import numpy as np
FIT = True
my_lattice = lattice.Lattice24c()
bfolder = '/temp/srd1g10/results/24c/baryons/0.005_0.005_0.04/'
bfolders = (bfolder+'pickled.b14.p16/', bfolder+'pickled.b15.p16/', bfolder+'pickled.b16.p16/')
bar = Baryon.load_from_folder(bfolders, fit_range=(10, 17),
                              name="$0.04^3$",
                              lattice=my_lattice,
                              fit_type='individual',
                              average_over_folders=True,
                              mass_guess=1.034,
                              covariant=True,
                              correlated=False, frozen_error=True,
                              num_bins=2, verbose=False)

def get_mass():
    bar.fit()
    return bar.get_jackknife_lists()

if __name__=="__main__":
    if FIT:
        bar.fit()
        print bar.get_fit_params()
        print bar.get_fit_params_latex()
    else:
        bar.plot_graph()


