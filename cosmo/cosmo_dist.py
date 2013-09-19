#!/usr/bin/env python

############################################################################################
#  Collection of routines for calculation of cosmological distances and related parameters #
#                                                                                          #

#  Changelog:
# 2013-06-17
# added w to t E(z) calculation (and hence to all distances), seems to
# work fine, but more testing could be good. Omega_R is currently just
# a mock up(i.e. 0, no passing yet added thogh should be very simple).
# The whole code should be rewriten a cosmology object


#  NOTE:                                                                                   #
# - all distances are in Mpc                                                               #
#                                                                                          #
#  AUTHOR: Robert Suhada                                                                   #
#  REFERENCE: Hogg, 99                                                                     #
#  http://arxiv.org/abs/astro-ph/9905116                                                   #
#                                                                                          #
#  FIXME:                                                                                  #
#  - add more/better array wrappers                                                        #
#  - dedicated ang. scale subroutine                                                       #
############################################################################################

from numpy import *
from scipy import integrate
c = float64(2.99792458e+5)                  #  speed of light in km/s

def resolve_curvature(omega_k_0, omega_m_0, omega_de_0):
    """
    Defaults to flat universe, if omega_k_0 is not specified
    """
    if (omega_k_0 == 999.999):
        omega_k_0 = 1.0 - omega_m_0 - omega_de_0

    return omega_k_0


def ez_func(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, omega_r=0.0, w=-1.0):
    """
    Calculates the E(z) = H(z)/h_0
    """
    # FIXME: add proper resolution for the radiation density
    omega_k_0 = resolve_curvature(omega_k_0, omega_m_0, omega_de_0)
    ez = sqrt(omega_m_0*(1+z)**3 + omega_k_0*(1+z)**2 + omega_r*(1+z)**4 + omega_de_0*(1+z)**(3*(1+w)))
    return ez


def div_ez_func(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    Retur 1.0/Ez required for the num. integration
    """
    omega_k_0 = resolve_curvature(omega_k_0, omega_m_0, omega_de_0)

    # FIXME: omega_r not supported yet
    omega_r = 0.0
    ez = sqrt(omega_m_0*(1+z)**3 + omega_k_0*(1+z)**2 + omega_r*(1+z)**4 + omega_de_0*(1+z)**(3*(1+w)))
    return 1.0/ez


def dist_hubble(z=0.0, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    D_H
    Calculates the Hubble distance D_H = c/H(z)
    """
    omega_k_0 = resolve_curvature(omega_k_0, omega_m_0, omega_de_0)
    # dh = c/(h_0*ez_func(z, h_0, omega_m_0, omega_de_0, omega_k_0))
    dh = c/h_0
    return dh


def dist_comov_rad(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    D_C
    Calculates the radial comoving distance at redshift z. Integration by Gaussian quadrature.
    """
    dc = 0.0
    if (z==0.0):
        dc = 0.0
    else:
        dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
        (integrand, error) = integrate.quadrature(div_ez_func, 0.0, z, args=(h_0, omega_m_0, omega_de_0, omega_k_0, w), tol=1.5e-9, maxiter=1000)
        dc = dh * integrand
    return dc


def dist_comov_trans(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    D_M
    Calculates the radial transverse distance at redshift z. Integration by Gaussian quadrature.
    """

    omega_k_0 = resolve_curvature(omega_k_0, omega_m_0, omega_de_0)

    if (omega_k_0 == 0.0):
        dm = dist_comov_rad(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    elif (omega_k_0 > 0.0):
        dc = dist_comov_rad(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
        dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
        fact = sinh(sqrt(omega_k_0)*dc/dh)
        dm = dh*fact/sqrt(omega_k_0)
    elif (omega_k_0 < 0.0):
         dc = dist_comov_rad(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
         dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
         fact = sin(sqrt(abs(omega_k_0))*dc/dh)
         dm = dh*fact/sqrt(abs(omega_k_0))
    return dm


def dist_ang(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    D_A
    Calculates the angular distance [Mpc] (Carroll et al. 92)
    at given redshift and cosmology.
    """
    da = pow(1+z, -1)*dist_comov_trans(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    return da


def dist_lum(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    D_L
    Calculates the luminosoty distance [Mpc] (Carroll et al. 92)
    at given redshift and cosmology.
    """
    dl = (1+z)*dist_comov_trans(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    return dl


def comov_vol(z=0.0, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    Gives the full sky comoving volume integrated to redshift z.
    """
    omega_k_0 = resolve_curvature(omega_k_0, omega_m_0, omega_de_0)

    dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    dm = dist_comov_trans(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    rd=dm/dh

    if omega_k_0 > 0.0:
        a = 4.0*pi*dh**3/(2.0*omega_k_0)
        b = rd*sqrt(1+omega_k_0*rd**2)
        c = arcsinh(sqrt(abs(omega_k_0))*rd)/sqrt(abs(omega_k_0))
        vz=a*(b-c)
    elif omega_k_0 == 0.0:
        vz=4.0*pi*dm**3/3.0
    elif omega_k_0 < 0.0:
        a = 4.0*pi*dh**3/(2.0*omega_k_0)
        b = rd*sqrt(1+omega_k_0*rd**2)
        c = arcsin(sqrt(abs(omega_k_0))*rd)/sqrt(abs(omega_k_0))
        vz=a*(b-c)

    return vz

def dvdz(z=0.5, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):
    """
    Calculate the infinitesimal comov volume element at redshift z
    """
    dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    ez = ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    out = (da**2 * dh * (1+z)**2)/(ez)

    return out

#######################################################
# batch versions - able to process arrays of z
# FIXME: works but ugly solution

def batch_dist_ang(z, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):

    da = ones(len(z), dtype=float32)

    for i in range(0, len(z)):
        dai = dist_ang(z=z[i], h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
        da[i] = dai

    return da

def batch_dist_lum(z, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, w=-1.0):

    dl = empty(len(z), dtype=float32)

    for i in range(0, len(z)):
        dl[i] = dist_lum(z=z[i], h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)

    return dl

######################################################################
# main
######################################################################


if __name__ == '__main__':
    print "ok"

    # FIXME: should be rewritten using objects! (great learning example)

    ##############################
    # TEST PART
    ##############################

    w=-0.5
    z=3.0
    h_0=70.0
    omega_m_0=0.3
    omega_de_0=0.7
    omega_k_0=0.0

    ez=ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    dc = dist_comov_rad(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    dm = dist_comov_trans(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)
    dl = dist_lum(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, w=w)

    ##############################
    # OUTPUT
    ##############################

    print 'z        :: ', z
    print 'h_0      :: ', h_0
    print 'omega_m_0 :: ', omega_m_0
    print 'omega_de_0 :: ', omega_de_0
    print 'omega_k_0 :: ', omega_k_0
    print 'w         :: ', w
    print
    print 'ez :: ', ez
    print 'dh :: ', dh
    print 'dc :: ', dc
    print 'dm :: ', dm
    print 'da :: ', da
    print 'dl :: ', dl
    print

    # # no curvature set
    # ez=ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, w=w)
    # dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, w=w)
    # dc = dist_comov_rad(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, w=w)
    # dm = dist_comov_trans(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, w=w)
    # da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, w=w)
    # dl = dist_lum(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, w=w)

    # ##############################
    # # OUTPUT
    # ##############################

    # print 'z        :: ', z
    # print 'h_0      :: ', h_0
    # print 'omega_m_0 :: ', omega_m_0
    # print 'omega_de_0 :: ', omega_de_0
    # print 'omega_k_0 :: ', omega_k_0
    # print
    # print 'ez :: ', ez
    # print 'dh :: ', dh
    # print 'dc :: ', dc
    # print 'dm :: ', dm
    # print 'da :: ', da
    # print 'dl :: ', dl
    # print
