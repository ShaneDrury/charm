import numpy as np
import Gnuplot
Gnuplot.GnuplotOpts.prefer_inline_data = 1  # To fix zooming
import m24_0_005_0_005, m24_0_01_0_01, m24_0_0348_0_0348, m24_0_04_0_04, m24_0_0613_0_0613, m24_0_10177_0_10177, m24_0_123_0_123
all = [m24_0_005_0_005, m24_0_01_0_01, m24_0_0348_0_0348, m24_0_04_0_04, m24_0_0613_0_0613, m24_0_10177_0_10177, m24_0_123_0_123]

c=[]
c_err=[]
masses = []
a_inv = 1.73 # GeV
for a in all:
    cc, cce, mass = a.get_c()
    print cc, cce, mass * a_inv
    c.append(cc)
    c_err.append(cce)
    masses.append(mass * a_inv)

g = Gnuplot.Gnuplot(persist=True)
g.title('Dispersion Relation Breakdown - Heavy-Heavy Uncorrelated Fit')
g('set style data errorbars')
g('set xlabel "Heavy-Heavy Meson Mass (GeV)"')
g('set ylabel "c^2"')
data = Gnuplot.Data(zip(masses, c, c_err))
th = [1.0 for x in masses]
theory = Gnuplot.Data(zip(masses, th), with_='lines lt 2')
#theory = Gnuplot.Data(zip(masses, th))

#g('set output "my-plot.ps"')
g.plot(data, theory)
g.hardcopy('my-plot-heavy-heavy-uncorrelated.eps', enhanced=1, color=1)


#data = Gnuplot.Data(zip(x, y, error))
#g('set xrange [0:{T}]'.format(T=T/2))
