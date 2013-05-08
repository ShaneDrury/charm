import numpy as np
import Gnuplot
from pyon import glob_consts
import minuit
charm_masses = np.array([0.005, 0.0348, 0.04, 0.0472, 0.055, 0.0613, 0.07, 0.1, 0.10177, 0.12, 0.123, 0.132])
meson_masses = [0.330559280664, 0.54511303046, 0.574929281824, 0.614095114864, 0.654246552928, 0.685228873254, 0.726221292942, 0.855401143241, 0.862543732666, 0.933672056314, 0.944974978083, 0.978289482028]
a_inv = 1.73 # GeV
charm_masses = charm_masses +glob_consts.mres24
meson_masses = np.array(meson_masses )#/ a_inv
g = Gnuplot.Gnuplot(persist=True)
data = Gnuplot.Data(zip(charm_masses, meson_masses))
g.plot(data)
target = 1.15**2

def functional(x, A, B):
    return A * x + B
    
def chi_sq(A, B):
    return (target - functional(A, B))**2


