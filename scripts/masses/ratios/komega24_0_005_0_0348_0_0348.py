from pyon.Error.error_reduce import mean_and_error
from pyon.IO import prettify
import numpy as np
FIT=True
from charm.scripts.masses.mesons import m24_0_005_0_0348 as m24
from charm.scripts.masses.baryons import b24_0_0348 as b24

FIT = True
def get_ratio():
    mjl = m24.get_mass()
    bjl = b24.get_mass()
    return mjl/bjl

if __name__ == "__main__":
    if FIT:
        print "Meson"
        mjl = m24.get_mass()
        print m24.mes.get_fit_params()
        print m24.mes.get_fit_params_latex()
        print "Baryon"
        bjl = b24.get_mass()
        print b24.bar.get_fit_params()
        print b24.bar.get_fit_params_latex()
        ratiojl = mjl/bjl
        central, error = mean_and_error(ratiojl)
        print "m_K / m_omega"
        print central, error
        print m24.mes.name + ",", b24.bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"
    else:
        mes.plot_graph()
        bar.plot_graph()
