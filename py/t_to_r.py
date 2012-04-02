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

def write_par_output(tofile=0):
    """
    Output current set of parameters to scree/file
    FIXME: add TeX/HTML formats to output.
    """
    if (tofile==0):
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
        print  't_fit        ', t
        print  't_fit_err_n  ', t_err_n
        print  't_fit_err_p  ', t_err_p
        print  'z            ', z
        print  'z_err_n      ', z_err_n
        print  'z_err_p      ', z_err_p
        print  'abund        ', abund
        print  'abund_err_n  ', abund_err_n
        print  'abund_err_p  ', abund_err_p
        print
        print  'yx500        ', yx500
        print  'yx500_err    ', yx500_err
        print  'ysz500       ', ysz500
        print  'ysz500_err   ', ysz500_err
        print
        print  't500         ', t500
        print  't500_err     ', t500_err
        print  'm500         ', m500
        print  'm500_err     ', m500_err
        print  'r500         ', r500
        print  '0.15r500_ang ', 0.15*r500_ang
        print  'r500_ang     ', r500_ang
        print
        print  'rfit_ang     ', rfit_ang

    else:
        fname = "formated_pars.out"
        f = open(fname, 'w')
        round_to = 1

        f.write('h_0          %4.1f\n' % (h_0))
        f.write('omega_m_0    %5.3f\n' % (omega_m_0))
        f.write('omega_de_0   %5.3f\n' % (omega_de_0))
        f.write('omega_k_0    %5.3f\n' % (omega_k_0))
        f.write('')
        f.write('Ez           %5.3f\n' % (ez))
        f.write('')
        f.write('norm         %4.2e\n' % (norm))
        f.write('norm_err_n   %4.2e\n' % (norm_err_n))
        f.write('norm_err_p   %4.2e\n' % (norm_err_p))
        f.write('t_fit        %3.1f\n' % (t))
        f.write('t_fit_err_n  %3.1f\n' % (t_err_n))
        f.write('t_fit_err_p  %3.1f\n' % (t_err_p))
        f.write('z            %5.3f\n' % (z))
        f.write('z_err_n      %5.3f\n' % (z_err_n))
        f.write('z_err_p      %5.3f\n' % (z_err_p))
        f.write('abund        %4.2f\n' % (abund))
        f.write('abund_err_n  %4.2f\n' % (abund_err_n))
        f.write('abund_err_p  %4.2f\n' % (abund_err_p))
        f.write('')
        f.write('yx500        %4.2e\n' % (yx500))
        f.write('yx500_err    %4.2e\n' % (yx500_err))
        f.write('ysz500       %4.2e\n' % (ysz500))
        f.write('ysz500_err   %4.2e\n' % (ysz500_err))
        f.write('')
        f.write('t500         %3.1f\n' % (t500))
        f.write('t500_err     %3.1f\n' % (t500_err))
        f.write('m500         %4.2e\n' % (m500))
        f.write('m500_err     %4.2e\n' % (m500_err))
        f.write('r500         %3.1f\n' % (r500))
        f.write('0.15r500_ang %4.1f\n' % (0.15*r500_ang))
        f.write('r500_ang     %4.1f\n' % (r500_ang))
        f.write('')
        f.write('rfit_ang     %4.1f\n' % (rfit_ang))
        f.close()


if __name__ == '__main__':
    """
    Convert a temperature estimate to a mass and turn it to an aperture.

    Local settings:
    - cosmological parameters
    - pick scaling relations
    """

    FILE_PAR_OUTPUT=1          # write rounded output to file?

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
    # choice of scaling relations
    #
    # 1
    # - T500-M vikhlinin 09, analytic r500
    #
    # 2
    # - 0.5 T500-T500 vikhlinin09, T500-M vikhlinin 09, analytic r500

    SCALING_OPTION=1
    ######################################################################
    # read in the spectrospopy results

    parfile = sys.argv[1]
    results = read_xspec_result_file(parfile)

    norm = float(results[0])
    norm_err_n = float(results[1])
    norm_err_p = float(results[2])

    t = float(results[3])
    t_err_n = float(results[4])
    t_err_p = float(results[5])

    z = float(results[6])
    z_err_n = float(results[7])
    z_err_p = float(results[8])

    abund = float(results[9])
    abund_err_n = float(results[10])
    abund_err_p = float(results[11])

    t = float(t)
    t_err = 0.5 * (abs(float(t_err_n)) + float(t_err_p))
    z = float(z)

    ######################################################################
    # do the calculations

    print
    print '######################################################################'
    print 'Results:'

    ez = ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0) # [Mpc]
    ang_scale = da * math.tan(math.pi/(180.0*3600.0))            # [Mpc/asec]

    if (SCALING_OPTION == 1):
        print "Scaling relation chain : ", SCALING_OPTION
        (t500, t500_err) = (t, t_err)
        (m500, m500_err) = scal_rel_lib.MT_vikhlinin09(t, t_err, ez, h) # [Msol]

        (yx500, yx500_err) = scal_rel_lib.MYx_vikhlinin09(m500, m500_err, ez, h)
        (ysz500, ysz500_err) = scal_rel_lib.MYsz_andersson11(m500, m500_err, ez)

        r500 = scal_rel_lib.r_overdensity(overdensity, m500, m500_err, ez)[0] # [Mpc]
        r500_ang = r500 / ang_scale # [asec]
        rfit_ang = r500_ang

    elif (SCALING_OPTION == 2):
        print "Scaling relation chain : ", SCALING_OPTION
        (t500, t500_err) = scal_rel_lib.TT_vikhlinin09(t, t_err)
        (m500, m500_err) = scal_rel_lib.MT_vikhlinin09(t500, t500_err, ez, h) # [Msol]

        (yx500, yx500_err) = scal_rel_lib.MYx_vikhlinin09(m500, m500_err, ez, h)
        (ysz500, ysz500_err) = scal_rel_lib.MYsz_andersson11(m500, m500_err, ez)

        r500 = scal_rel_lib.r_overdensity(overdensity, m500, m500_err, ez)[0] # [Mpc]
        r500_ang = r500 / ang_scale # [asec]
        rfit_ang = 0.5 * r500_ang   # fit only in the half aperture

    ######################################################################
    # output

    write_par_output()
    if (FILE_PAR_OUTPUT==1):
        write_par_output(tofile=1)

