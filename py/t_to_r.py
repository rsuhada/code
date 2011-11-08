#!/usr/bin/env python
import sys
import os
import math
import string
from numpy import *
from cosmo_dist import ez_func, dist_ang
import scal_rel_lib


def read_xspec_result_file(infile):
    """
    Reads in the xspec result file and returns the parameters
    Arguments:
    - `infile`: xspec result outpyt log

    """

    input_file = open(infile)
    results_txt = input_file.readlines()
    input_file.close()

    results = []

    for line in results_txt:
        item = string.split(line," ")
        results.append(item[1])
        results.append(item[2])
        results.append(item[3])

    return results


if __name__ == '__main__':
    """
    Convert a temperature estimate to a mass and turn it to an aperture.

    Local settings:
    - cosmological parameters
    - pick scaling relations
    """

    ######################################################################
    # cosmology settings
    # FIXME: cosmology has to be centralized in a conf file - also
    # relevant for the xspec spectroscopy scripts

    h_0 = 70.0
    omega_m_0 = 0.3
    omega_de_0 = 0.7
    omega_k_0 = 0.0
    overdensity = 500.0         # with respect to critical density

    h = h_0/100.0

    ######################################################################
    # read in the spectrospopy results

    parfile = sys.argv[1]
    # parfile = "/Users/rs/w/xspt/data/SPT-CL-J0205-5829/iter-spec/run-001-iter-r-037/SPT-CL-J0205-5829-iter-r-037-001.result"

    results = read_xspec_result_file(parfile)

    norm = results[0]
    norm_err_n = results[1]
    norm_err_p= results[2]

    t = results[3]
    t_err_n = results[4]
    t_err_p= results[5]

    z = results[6]
    z_err_n = results[7]
    z_err_p= results[8]

    abund = results[9]
    abund_err_n = results[10]
    abund_err_p= results[11]

    t = float(t)
    t_err = 0.5 * (abs(float(t_err_n)) + float(t_err_p))
    z = float(z)

    ######################################################################
    # do the calculations

    ez = ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0) # [Mpc]
    ang_scale = da * math.tan(math.pi/(180.0*3600.0))            # [Mpc/asec]

    (m500, m500_err) = scal_rel_lib.MT_vikhlinin09(t, t_err, ez, h) # [Msol]

    r500 = scal_rel_lib.r_overdensity(overdensity, m500, m500_err, ez)[0] # [Mpc]
    r500_ang = r500 / ang_scale # [asec]

    ######################################################################
    # output

    print
    print  'h_0          ', h_0
    print  'omega_m_0    ', omega_m_0
    print  'omega_de_0   ', omega_de_0
    print  'omega_k_0    ', omega_k_0
    print
    print  'Ez           ', ez
    print
    print  'norm         ', norm
    print  'norm_err_n   ', norm_err_n
    print  'norm_err_p   ', norm_err_p
    print  't            ', t
    print  't_err_n      ', t_err_n
    print  't_err_p      ', t_err_p
    print  'z            ', z
    print  'z_err_n      ', z_err_n
    print  'z_err_p      ', z_err_p
    print  'abund        ', abund
    print  'abund_err_n  ', abund_err_n
    print  'abund_err_p  ', abund_err_p
    print
    print  'm500         ', m500
    print  'm500_err     ', m500_err
    print  'r500         ', r500
    print  '0.15r500_ang ', 0.15*r500_ang
    print  'r500_ang     ', r500_ang



