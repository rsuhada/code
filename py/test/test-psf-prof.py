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
from sb_plotting_utils import *
from sb_utils import *


if __name__ == '__main__':
    print

    # PSF testing
    energy = 1.5
    theta = 0.3

    instrument=("pn", "m1", "m2")

    plot_king_model_psf(energy, theta, instrument)

    for i in instrument:
        print i
        (rcore, alpha) = get_psf_king_pars(i, energy, theta)
        print rcore, alpha

    print "done"

    # plt.show()
