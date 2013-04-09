#!/usr/bin/env python
from numpy import *
from cosmo_dist import dist_ang
from physconstants import *
from scipy import integrate

def beta_shape_integral(rho, zeta, beta):
    """
    Beta model shape integral. Integral was validated with
    Mathematica.

    Arguments:
    - `rho`: dimensionless projected radius (squared)
    - `zeta`: dimensionless LOS distance
    - `beta`: beta power
    """
    return (1 + rho + zeta**2)**(-3*beta)

def v06mod_shape_integral(rho, zeta, a, beta, gamma, epsilon, rbar):
    """
    Modified Vikhlinin06 model shape integral. Integral was validated
    with Mathematica.

    - `rho`: dimensionless projected radius (squared)
    - `zeta`: dimensionless LOS
    - 'a': alpha/2 - power from the profile
    - 'beta', 'gamma', 'epsilon': powers from the profile
    """
    x = rho + zeta**2
    i = x**(-a) * (1 + x)**(a - 3.0*beta) * (1 + x**(gamma/2.0) * rbar)**(-1.0*epsilon/gamma)

    return i

def spec_norm_to_density(norm, z, da, rproj1_ang, rproj2_ang, model_name, model_pars):
    """
    Convert XSPEC normalization to density for a spherical region,
    optionally with excised inner sphere.

    Arguments:
    - `norm`: XSPEC normalization in XSPEC units
    - `z`: redsihift
    - `da`: angular diameter distance [Mpc]
    - `rproj1_ang`: projected radius of the inner
                    excised spherical region [arcsec]
    - `rproj2_ang`: projected outer radius of the fitted spherical
                    region [arcsec]
    - `model_name`: model identifier: beta, v06
    - 'model_pars': parameter structure - content depends on : on the model

    Output:
    - `density`: density in cgs [g cm**-3]
    """

    # get relative molecular weights: Feldman 1992, A=0.3
    mu_e = mu_e_feldman92
    mu_h = mu_h_feldman92

    # convert everything to cgs
    da = da * mpc_to_cm

    # the constant factor
    const = norm * 2 * mu_e * mu_h * mp_cgs**2 * (da*(1+z))**2 * 1.0e14
    integ_profile = 1.0

    if model_name == 'beta':
        print 'Using beta model'

        rcore = model_pars[0]
        beta  = model_pars[1]

        print 'rcore: ', rcore
        print 'beta: ', beta
        print

        # integration bounds
        rho1 = (rproj1_ang / rcore)**2
        rho2 = (rproj2_ang / rcore)**2

        # do the integration
        # for rmax in (1, 1.0e2, 1.0e5, 1.0e6, Inf):
        for rmax in (Inf,):
            integ_profile = integrate.dblquad(beta_shape_integral, 0.0, rmax,
                                              lambda rho:rho1, lambda rho:rho2,
                                              args=(beta,))[0]
            print "Integration bound :: ", rmax, 'Shape integral :: ', integ_profile
            integ_profile = integ_profile * (rcore * arcsec_to_radian * da)**3


    elif model_name == 'v06mod':
        print 'Using modified v06 model'

        # unpack parameters
        alpha   = model_pars[0]
        beta    = model_pars[1]
        gamma   = model_pars[2]
        epsilon = model_pars[3]
        rc      = model_pars[4]
        rs      = model_pars[5]

        a = alpha / 2.0
        rbar = (rc/rs)**gamma

        # integration bounds
        rho1 = (rproj1_ang / rc)**2
        rho2 = (rproj2_ang / rc)**2

        # do the integration
        # for rmax in (1, 1.0e2, 1.0e5, 1.0e6, Inf):
        for rmax in (Inf,):
            integ_profile = integrate.dblquad(v06mod_shape_integral, 0.0, rmax,
                                              lambda rho:rho1, lambda rho:rho2,
                                              args=(a, beta, gamma, epsilon, rbar))[0]
            print "Integration bound :: ", rmax, '   shape integral :: ', integ_profile
            integ_profile = integ_profile * (rc * arcsec_to_radian * da)**3

    try:
	density = sqrt(const / integ_profile)
    except Exception, e:
	raise e

    return density


if __name__ == '__main__':
    print
    ######################################################################
    # test normalization calculation

    TEST_MODEL_NAME = 'beta'    # beta, v06mod
    # TEST_MODEL_NAME = 'v06mod'    # beta, v06mod

    # cosmology
    h_0=70.2
    omega_m_0=0.272
    omega_de_0=0.728
    omega_k_0=0.0

    # cluster
    z = 0.468
    rproj1_ang = 0.0   # projected radius [arcsec]
    rproj2_ang = 60.0    # projected radius [arcsec]

    norm = 1.45738E-03          # xspec norm
    norm_err_n = -4.5767e-05
    norm_err_p = +4.53208e-05

    # setup the parameters for the integration
    if TEST_MODEL_NAME == 'beta':
        model_name = TEST_MODEL_NAME

        # best fit parameters should go here
        rcore = 10.0 * 2.5                # [arcsec]
        beta  = 2.0/3.0
        model_pars = (rcore, beta)

    elif TEST_MODEL_NAME == 'v06mod':
        model_name = TEST_MODEL_NAME

        rc = 20.0                   # ballpark 0.1 r500
        beta = 2.0/3.0
        rs = 20.0                   # ballpark 0.5-1 r500
        alpha = 1.5                 # <3
        gamma = 3.0                 # fix = 3
        epsilon = 2.0               # <5

        model_pars = (alpha, beta, gamma, epsilon, rc, rs)


    # angular distance
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0) # [Mpc]
    angscale = arcsec_to_radian * da * 1000.0 # [kpc/arcsec]

    # do the integration
    density = spec_norm_to_density(norm, z, da, rproj1_ang, rproj2_ang, model_name, model_pars)
    ne = density / (mu_e_feldman92 * mp_cgs)

    print
    print " z          :: ", z
    print " da         :: ", da
    print " ang scale  :: ", angscale
    print " norm       :: ", norm
    print " density    :: ", density
    print " ne density :: ", ne





