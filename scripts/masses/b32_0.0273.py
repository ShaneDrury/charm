from pyon.Classes.hadron import Baryon
from pyon.Classes import lattice

#from pyon.Error import error_reduce
#import numpy as np
my_lattice = lattice.Lattice32c()
bfolder = '/export/scratch/srd1g10/results/32c/baryons/0.006_0.006_0.0273/'
bfolders = (bfolder+'pickled.b14.p16/', bfolder+'pickled.b15.p16/', bfolder+'pickled.b16.p16/')
bar = Baryon.load_from_folder(bfolders, fit_range=(11, 23),
                              name="0.0273",
                              lattice=my_lattice,
                              fit_type='individual',
                              average_over_folders=True,
                              mass_guess=0.776,
                              covariant=True,
                              correlated=False, frozen_error=True,
                              num_bins=2, verbose=False)


if bar.fit():
    print bar.get_fit_params()
    print bar.get_fit_params_latex()
    #bar.plot_graph()


