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

def king_profile(r, rcore, alpha):
    """
    Returns a king profile on the input grid

    Arguments:
    - `r`: input radii [arcsec]
    - 'rcore': King model core radius [arcsec]
    - 'alpha': King model slope
    """

    y = 1 / ( 1 + (r/rcore)**2 )**alpha

    return y


def plot_model_psf(energy, theta, instrument):
    """
    Makes a plot of the psf model

    Arguments:
    - `energy`: energy [keV]
    - `theta`: off-axis angle [arcmin]
    - `instrument`: "m1", "m2", "pn", [set]
    """
    rmax


    if ("m1" in instrument):
        (rcore, alpha) = get_psf_prof(instr, energy, theta)
        print "plotting m1"

    if ("m2" in instrument):
        print "plotting m2"
        (rcore, alpha) = get_psf_prof(instr, energy, theta)

    if ("pn" in instrument):
        print "plotting pn"
        (rcore, alpha) = get_psf_prof(instr, energy, theta)

if __name__ == '__main__':
    print

    energy = 1.5
    theta = 1.0

    instrument=("pn", "m1", "m2")
    # instrument=("m1",)

    plot_model_psf(energy, theta, instrument)

    for i in instrument:
        print i
        (rcore, alpha) = get_psf_king_pars(i, energy, theta)
        print rcore, alpha

    print "done"
