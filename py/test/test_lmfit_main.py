#!/usr/bin/env python
import sys
import os
import math
import pyfits
from numpy import *
from pylab import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator

from lmfit import minimize, Parameters
import numpy as np
from pylab import random

def mymodel(x, params):
    amp = params['amp'].value
    shift = params['phase_shift'].value
    omega = params['omega'].value
    decay = params['decay'].value

    return amp * np.sin(x * omega + shift) * np.exp(-x*x*decay)

def residual(params, x, data=None):
    """
    Define the residual
    If data == None, return the model.
    """

    model = mymodel(x, params)

    if data == None:
        return model
    return (data-model)

params = Parameters()
true_params = Parameters()

# make mock data using the fit model
true_params.add('amp', value=20)
true_params.add('decay', value=0.01, vary=False)
true_params.add('phase_shift', value=0.5)
true_params.add('omega', value=2.0)

x = np.arange(0.0, 10.0, 0.5)
data = mymodel(x, true_params)
data = data + random(data.shape)

# fit initialization
params.add('amp', value=10)
params.add('decay', value=0.01, vary=True)
params.add('phase_shift', value=0.2)
params.add('omega', value=4.0)

# params['amp'].value=10
# params['decay'].value=0.007
# params['phase_shift'].value=0.2
# params['omega'].value=3.0

result = minimize(residual, params, args=(x, data))

# print result.chisqr
print
print
print 'True Values:'
for name, par in true_params.items():
    print '  %s = %.4f' % (name, par.value)

print
print 'Best-Fit Values:'
for name, par in params.items():
    print '  %s = %.4f +/- %.4f ' % (name, par.value, par.stderr)

xx = np.arange(0.0, 10.0, 0.05)
fitted_model = mymodel(xx, params)
true_model = mymodel(xx, true_params)


# interactive quick plot
plt.figure()
plt.ion()
plt.clf()

plt.plot(x, data,
    color='black',
    linestyle='',              # -/--/-./:
    linewidth=1,                # linewidth=1
    marker='o',                  # ./o/*/+/x/^/</>/v/s/p/h/H
    markerfacecolor='black',
    markersize=8,               # markersize=6
    label=r"data"               # '__nolegend__'
    )

plt.plot(xx, fitted_model,
    color='red',
    linestyle='-',              # -/--/:/-.
    linewidth=2,                # linewidth=1
    marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
    markerfacecolor='black',
    markersize=0,               # markersize=6
    label=r"model"               # '__nolegend__'
    )

plt.plot(xx, true_model,
    color='green',
    linestyle='-',              # -/--/:/-.
    linewidth=2,                # linewidth=1
    marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
    markerfacecolor='black',
    markersize=0,               # markersize=6
    label=r"true"               # '__nolegend__'
    )

plt.legend()
plt.xscale("linear")
plt.yscale("linear")

plt.show()
plotPosition="+640+0"          # large_screen="+1100+0"; lap="+640+0"
plt.get_current_fig_manager().window.wm_geometry(plotPosition)




