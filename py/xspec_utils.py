#!/usr/bin/env python
from numpy import *
from cosmo_dist import dist_ang
from physconstants import *
from scipy import integrate

def beta_shape_integral(rho, zeta, beta):
    """
    Beta model shape integral

    Arguments:
    - `rho`: dimensionless projected radius (squared)
    - `zeta`: dimensionless LOS distance
    - `beta`: beta power
    """
    return (1 + rho + zeta**2)**(-3*beta)

def v06mod_shape integral(rho, zeta, a, beta, gamma, epsilon, rbar);
    """
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

    # go on with pomodoros as you like
    # rproj1 = rproj1_ang * arcsec_to_radian * da       # [cm]
    # rproj2 = rproj2_ang * arcsec_to_radian * da       # [cm]

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
        for rmax in (1, 1.0e2, 1.0e5, 1.0e6, Inf):
            integ_profile = integrate.dblquad(beta_shape_integral, 0.0, rmax, lambda rho:rho1, lambda rho:rho2, args=(beta,))[0]
            print rmax, integ_profile

        integ_profile = integ_profile * (rcore * arcsec_to_radian * da)**3

    elif model_name == 'v06':
        print 'Using v06 model'
    try:
	density = sqrt(const / integ_profile)
    except Exception, e:
	raise e


    return density


if __name__ == '__main__':
    print
    ######################################################################
    # test normalization calculation

    # cosmology
    h_0=70.2
    omega_m_0=0.272
    omega_de_0=0.728
    omega_k_0=0.0

    # cluster
    z = 0.468
    rproj1_ang = 0.0   # projected radius [arcsec]
    rproj2_ang = 60.0    # projected radius [arcsec]
    model_name = 'beta'
    rcore = 10.0 * 2.5                # [arcsec]
    beta  = 2.0/3.0
    model_pars = (rcore, beta)

    norm = 1.45738E-03          # xspec norm
    norm_err_n = -4.5767e-05
    norm_err_p = +4.53208e-05


    # angular distance
    da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0) # [Mpc]
    angscale = arcsec_to_radian * da * 1000.0 # [kpc/arcsec]

    density = spec_norm_to_density(norm, z, da, rproj1_ang, rproj2_ang, model_name, model_pars)
    ne = density / (mu_e_feldman92 * mp_cgs)

    print
    print " z          :: ", z
    print " da         :: ", da
    print " ang scale  :: ", angscale
    # print " rproj1_ang :: ", rproj1_ang
    # print " rproj1     :: ", rproj1
    # print " rproj2_ang :: ", rproj2_ang
    # print " rproj2     :: ", rproj2
    print " norm       :: ", norm
    print " density    :: ", density
    print " ne density :: ", ne





