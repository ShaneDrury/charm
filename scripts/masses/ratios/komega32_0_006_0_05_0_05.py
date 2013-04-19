from pyon.Error.error_reduce import mean_and_error
from pyon.IO import prettify
import numpy as np
from charm.scripts.masses.mesons import m32_0_006_0_05 as m32
from charm.scripts.masses.baryons import b32_0_05 as b32

FIT = True
def get_ratio():
    mjl = m32.get_mass()
    bjl = b32.get_mass()
    return mjl/bjl

if __name__ == "__main__":
    if FIT:
        print "Meson"
        mjl = m32.get_mass()
        print m32.mes.get_fit_params()
        print m32.mes.get_fit_params_latex()
        print "Baryon"
        bjl = b32.get_mass()
        print b32.bar.get_fit_params()
        print b32.bar.get_fit_params_latex()
        ratiojl = mjl/bjl
        central, error = mean_and_error(ratiojl)
        print "m_K / m_omega"
        print central, error
        print m32.mes.name + ",", b32.bar.name, "&", prettify.bracket_error(central, error), "\\\ \hline"
    else:
        mes.plot_graph()
        bar.plot_graph()


