############################################################################################
#  Collection of routines for calculation of cosmological distances and related parameters #
#                                                                                          #
#  NOTE:                                                                                   #
# - works only for w=-1=const.                                                             #
# - all distances are in Mpc                                                               #
#                                                                                          #
#  AUTHOR: Robert Suhada                                                                              #
#                                                                                          #
#  FIXME:                                                                                  #
#  - clean up needed                                                                       #
############################################################################################


from numpy import *
from cosmo_dist import *
from math import pi
"""
validation wrt icosmos:
- ez, da, dl, covol
- omega_m_z

validated wrt hogg99:
- comov element

validated F_PS and F_J:
- wrt the jenkins01 plots (see multiplicityfunc.py)
"""

# const
c = float64(2.99792458e+8)                # [m/s]
G = float64(6.67300e-11)                  # m**3/kg/s**2
m2mpc = float64(1.0/3.08568025e+22)
kg2msol = float64(1.0/1.98892e+30)


def sugiyama_gamma(h_0=70, omega_m_0=0.3, omega_b_0=0.05):
    """
    Sugiyama 95 gamma function - the shape paramater for power spectrum transfer function in CDM cosmology
    It seems there are some typos, dunno what's the proper formula atm but
    """
    h = h_0/100.0
    # sugiyama_gamma = omega_m_0*h*exp(-1.0*omega_b_0*(1.0 + sqrt(2.0*h)/omega_m_0))  # sugiyama95 + sahlen08
    # sugiyama_gamma = omega_m_0*h*exp(-1.0*omega_b_0*(1.0 + 1.0/omega_m_0))          # viana96 - typo?!
    sugiyama_gamma = 0.18 # SDSS observations, e.g szalay03
    return sugiyama_gamma


def omega_m_z_func(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999):
    """
    Calculates OmegaM(z)
    """
    omegaz = (1.0 + z)**3 * omega_m_0 * ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)**-2
    return omegaz


def rho_crit_func(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999):
    """
    Calculates the critical density of Universe for given redshift.
    OUT : [Msol/Mpc**3]
    """
    H = 1000.0*h_0*ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)   # m/s/Mpc
    rho = 3.0*H**2/(8.0*pi*G)
    # rho = rho*1000.0*(m2mpc**2)*1.e-6        # g/cm**3
    rho = rho * kg2msol/m2mpc                  # Msol/Mpc**3
    return rho


def rho_m_z_func(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999):
    """
    Calculates the matter density of Universe for given redshift.
    OUT : [Msol/Mpc**3]
    """
    rho_crit_0 = rho_crit_func(z=0.0, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    rho_m_0 =  omega_m_0*rho_crit_0
    rho_m_z = rho_m_0*(1+z)**3
    return rho_m_z


def growth_supress_lcdm(omega_m_z = 0.3):
    """
    Calculates the growth supression function for OmegaM(z) in LCDM
    """
    a0 = 2.5
    a1 = 1.0/70.0
    a2 = 209.0/104.0
    a3 = -1.0/140.0
    a4 = 1.0

    g = a0*omega_m_z/(a1 + a2*omega_m_z + a3*omega_m_z**2 + a4*omega_m_z**(4.0/7.0))
    return g


def mass2linscale(m=1.0e+15, rho_m_z = 4.0e+10):
    """
    Gives the comoving linear scale R corresponding to mass scale M
    """
    # rho_m_z = rho_m_0*(1+z)**3
    r = pow(3.0*m/(4.0*pi*rho_m_z), 1.0/3.0)
    return r    # check! - is this the correcter r? rho_m_z vs rho_m_0


def sigma_8_z_func(z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, sigma_8_0 = 0.75):
    """
    Calculates sigma 8 at given z for LCDM.
    """
    omegaz = omega_m_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    g0 = growth_supress_lcdm(omega_m_0)
    gz = growth_supress_lcdm(omegaz)

    sigma8_z = sigma_8_0 * gz /(g0*(1.0+z))
    return sigma8_z


def gamma_exp_func(r=1.0, h_0=70, omega_m_0=0.3, omega_b_0=0.05):
    """
    Returns the gamma exponent gamma(R) for the sigma(R,z) expansion around sigma8(z)
    """
    h = h_0/100.0
    gammaS = sugiyama_gamma(h_0=h_0, omega_m_0=omega_m_0, omega_b_0=omega_b_0)
    gexp = (0.3*gammaS + 0.2)*(2.92 + log10(r*h/8.0))
    return gexp


def sigma_m_z_func(m=1.0, z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, sigma_8_0 = 0.75):
    """
    Calculate sigma for mass scale R and redshift z - using approximation around sigma8 scale
    """
    h = h_0/100.0
    rho_m_z = rho_m_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    r = mass2linscale(m=m, rho_m_z = rho_m_z)
    gamma_r = gamma_exp_func(r=r, h_0=h_0, omega_m_0=omega_m_0, omega_b_0=omega_b_0)
    s8z = sigma_8_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
    srz = s8z * (r*h/8.0)**(-1.0*gamma_r)
    return srz ####check


def Dsigm_m_z_Dm_approx(m=1.0, z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999):
    """
    Analytic derivative of sigma(M,z) wrt M, from the approxiamtion around sigma8
    """
    # incorrect:
    # rho_m_0 = rho_m_z_func(z=0, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    # r = mass2linscale(m=m, rho_m_z = rho_m_0)
    # gamma_r = gamma_exp_func(r=r, h_0=h_0, omega_m_0=omega_m_0, omega_b_0=omega_b_0)
    # ds = 1.0 * gamma_r/(3.0*m)

    sigma_m_z = sigma_m_z_func(m=m, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
    gammaS = sugiyama_gamma(h_0=h_0, omega_m_0=omega_m_0, omega_b_0=omega_b_0)
    gfact = 2.92*(0.3*gammaS + 0.2)

    ds = -1.0 * sigma_m_z*gfact/(3.0*m)

    return ds


def jenkins(sigma_m_z = 0.8):
    """
    Jenkins et al. 2001, mass function. See paper for const. for different density contrasts etc.
    """
    A = 0.316       # 324*rhoM(z), LCDM-SO(324)
    B = 0.67        # 324*rhoM(z), LCDM-SO(324)
    eps = 3.82      # 324*rhoM(z), LCDM-SO(324)

    F = A*exp(-1.0*abs(-1.0*log(sigma_m_z)+B)**eps)
    return F


def press_schechter(sigma_m_z = 0.8):
    """
    Press-Schechter mass function.
    """
    deltac = 1.7       # density contrast for collaps in PS formalism. deltac = 1.7 from sims, deltac = 1.69 analytical for EdS

    F = sqrt(2.0/pi) * deltac * sigma_m_z**-1 * exp(-1.0*deltac**2/(2.0*sigma_m_z**2))
    return F


def tinker08(sigma_m_z = array((0.0)), z=0.0, delta=200.0):
    """
    Tinker et al. 2008, mass function. Has redshift evolution and overdensity level dependance.
    """
    if delta==200.0:
        A0 = 0.186
        a0 = 1.47
        b0 = 2.57
        c0 = 1.19

    alpha = 10.0**(-1.0*(0.75/log10(delta/75.0))**1.2)
    Az = A0*(1+z)**(-0.14)
    az = a0*(1+z)**(-0.06)
    bz = b0*(1+z)**(-alpha)
    cz = c0                                                   # no evol here

    F = 0.0 * sigma_m_z
    for i in range(len(sigma_m_z)):
        F[i] = Az * ((sigma_m_z[i]/bz)**(-az) + 1.0) * exp(-1.0*cz/sigma_m_z[i]**2)
    return F



def num_counts(m=1.0, mass_func='press_schechter', z=0.3, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, sigma_8_0=0.8):
    """
    Calculate the number counts n(M, z)
    """
    sigma_m_z = sigma_m_z_func(m=m, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)

    if mass_func == 'jenkins':
        F = jenkins(sigma_m_z = sigma_m_z)
    if mass_func == 'press_schechter':
        F = press_schechter(sigma_m_z = sigma_m_z)

    rho_m_z = rho_m_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    Dsigma_Dm = Dsigm_m_z_Dm_approx(m=m, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)

    nmz = -1.0 * F * rho_m_z * Dsigma_Dm / (m * sigma_m_z)
    return nmz


def mass_integrate_num_counts(mmin=1.0e+13, mass_func='press_schechter', z=0.0, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, sigma_8_0=0.8):
    out = integrate.quad(num_counts, mmin, Inf, args=(mass_func, z, h_0, omega_m_0, omega_de_0, omega_k_0, sigma_8_0))[0]
    #out = out * dvdz(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    return out


def n_z(mass_func='press_schechter', mmin=1.0, z=0.0, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, sigma_8_0=0.8):
    """
    Integrates the cluster numbr counts function n(M,z) at given z for M in (Mmin, Inf)
    """
    #(integral, error) = integrate.quadrature(lambda z: mass_integrate_num_counts, zmin, Inf, args=(mmin=mmin, mass_func=mass_func, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0), tol=1.5e-8, maxiter=50)
    massint = mass_integrate_num_counts(mmin=mmin, mass_func=mass_func, z=0.0, h_0=70.0, omega_m_0=0.3, omega_de_0=0.7, omega_k_0=999.999, sigma_8_0=0.8)
    out = massint * dvdz(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
    return out


def virial_overdensity(omegamz):
    """
    Calculate the virial overdensity factor delta_vir based on Bryan and Norman (1998)
    INPUT: Omega matter at cluster redshift Omega_M(z)
    OUTPUT: delta_vir

    NOTE: delta_vir is wrt mean matter density not critical density
    """
    x = omegamz - 1
    delta_vir = (18.0 * pi**2 + 82.0 * x - 39.0 * x**2) / (1  + x)
    return delta_vir

def c_bullock01(z=0.5, m_vir=1.0e14, m_star=2.112676e13):
    """
    Calculate the NFW concentration based on Bullock+01.
    INPUT:  redshift
            virial mass [Msol] - the real virial mass not the 200c or something (althogh the mass dependance is very weak)
            m_star [Msol] - m_star parameter from bullock01, for lcdm  m_star = 1.5e13 / (H0/100.0)
    """
    c = 9.0 * (1 + z)**(-1) * (m_vir / m_star)**(-0.13)
    return c


######################################################################
# main
######################################################################


if __name__ == '__main__':
    print "ok"

#      ###########################################################
#      ### TEST PART
#      ###########################################################
#
#      z = 0.75
#      m = 5e+14
#
#      skyarea=6.0                         # [deg**2]
#      mmin=1.0e+13                        # [Msol]
#      skyarea = skyarea * (pi/180.0)**2
#      mass_func = 'press_schechter'
#
#
#      h_0=70.0
#      omega_dm_0 = 0.25
#      omega_b_0 = 0.05
#      omega_m_0 = omega_dm_0 + omega_b_0
#      omega_de_0 = 0.7
#      omega_k_0 = 1.0 - omega_m_0 - omega_de_0
#      sigma_8_0 = 0.8
#
#      ez = ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      dh = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      dc = dist_comov_rad(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      dm = dist_comov_trans(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      da = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      dl = dist_lum(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      covol = comov_vol(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      covol_element = dvdz(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#
#      sgamma = sugiyama_gamma(h_0=h_0, omega_m_0=omega_m_0, omega_b_0=omega_b_0)
#      omega_m_z = omega_m_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#
#      rho_crit_0 = rho_crit_func(z=0.0, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      rho_m_0 = rho_m_z_func(z=0.0, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      rho_m_z = rho_m_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#
#      r0 = mass2linscale(m=m, rho_m_z = rho_m_0)
#      r  = mass2linscale(m=m, rho_m_z = rho_m_z)
#
#      sigma_8_z = sigma_8_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
#      sigma_m_z = sigma_m_z_func(m=m, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
#      Dsigma_Dm = Dsigm_m_z_Dm_approx(m=m, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#
#      nmz = num_counts(m=m, mass_func=mass_func, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
#      nz =  skyarea * n_z(mass_func=mass_func, mmin=m, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
#
#      testcalc=mass_integrate_num_counts(mmin=mmin, mass_func=mass_func, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
#
#      nz=2
#      ###############################################
#      ###     outs
#      ###############################################
#
#      print
#      print '________________________________________'
#      print
#      print "h_0         = ", h_0
#      print "omega_dm_0   = ", omega_dm_0
#      print "omega_b_0    = ", omega_b_0
#      print "omega_m_0    = ", omega_m_0
#      print "omega_de_0    = ", omega_de_0
#      print "omega_k_0    = ", omega_k_0
#      print "sigma_8_0    = ", sigma_8_0
#      print
#      print "z          = ", z
#      print "m          = ", m
#      print
#      print '========================================'
#      print 'ez :: ', ez
#      print 'hz :: ', ez*h_0
#      print 'dh :: ', dh
#      print 'dc :: ', dc
#      print 'dm :: ', dm
#      print 'da :: ', da
#      print 'dl :: ', dl
#      print 'Comoving volume :: ', "%e" % covol
#      print 'Comoving volume element :: ', "%e" % covol_element
#      print '========================================'
#      print "rho_crit_0  = ", "%e" % rho_crit_0
#      print "rho_m_0      = ", "%e" % rho_m_0
#      print '========================================'
#      print "SGamma     = ", sgamma
#      print "omega_m(z)  = ", omega_m_z
#      print "sigma8(z)  = ", sigma_8_z
#      print "sigma(m,z)  = ", sigma_m_z
#      print '========================================'
#      print 'mass scale = ', m
#      print 'Lin. scale(0) = ', r0
#      print 'Lin. scale(z)   = ', r
#      print
#      print 'n(m,z)     = ', nmz
#      print '________________________________________'
#      print
#      print testcalc
#
#
#      #############################################################################
#      # make check plot
#
#      npoints = 399
#
#      zgrid = linspace(0.0, 4.975, npoints)
#      # print zgrid
#
#      m=8.78e+13           # 4.7e+15 is 8Mpc at z=0.75, sigma_8_0=0.8
#      mass_func = 'press_schechter'
#
#      h_0=70.0
#      omega_dm_0 = 0.25
#      omega_b_0 = 0.05
#      omega_m_0 = omega_dm_0 + omega_b_0
#      omega_de_0 = 0.7
#      omega_k_0 = 1.0 - omega_m_0 - omega_de_0
#      sigma_8_0 = 0.8
#
#      ez    = zeros(npoints, dtype='double')
#      dh    = zeros(npoints, dtype='double')
#      dc    = zeros(npoints, dtype='double')
#      dm    = zeros(npoints, dtype='double')
#      da    = zeros(npoints, dtype='double')
#      dl    = zeros(npoints, dtype='double')
#      covol = zeros(npoints, dtype='double')
#      covol_element = zeros(npoints, dtype='double')
#      omega_m_z = zeros(npoints, dtype='double')
#      mass_int = zeros(npoints, dtype='double')
#      nz = zeros(npoints, dtype='double')
#
#
#
#
#      #    for i in range(npoints):
#      #        z = zgrid[i]
#      #
#      #        # ez[i]    = ez_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # dh[i]    = dist_hubble(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # dc[i]    = dist_comov_rad(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # dm[i]    = dist_comov_trans(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # da[i]     = dist_ang(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # dl[i]     = dist_lum(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # covol[i]  = comov_vol(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # covol_element[i] = dvdz(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        # omega_m_z[i] = omega_m_z_func(z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
#      #        mass_int[i] = mass_integrate_num_counts(mmin=1.0e+13, mass_func='press_schechter',z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
#      #        nz[i] = n_z(mass_func=mass_func, mmin=m, z=z, h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0, sigma_8_0=sigma_8_0)
#      #
#      #        # print z, da[i], dl[i], covol[i]#, ez[i]#, da[i]#, dl[i]
#      #        print zgrid[i], nz[i]
#      #
#      #
#      #    #############################################################################
#      #    # start plot enviroment
#      #    #############################################################################
#      #
#      #    from pylab import rc
#      #    import matplotlib.pyplot as plt
#      #    import matplotlib.font_manager
#      #    from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator
#      #
#      #    # start figure
#      #    rc('axes', linewidth=1.5)
#      #    fig_obj = plt.figure()
#      #    fig_name='test.png'
#      #    headline_text = fig_obj.text(0.5, 0.95, '',
#      #               horizontalalignment='center',
#      #               fontproperties=matplotlib.font_manager.FontProperties(size=16))
#      #
#      #
#      #    ax1 = fig_obj.add_subplot(111)                         # rows/cols/num of plot
#      #    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault 0.2, 0.001 for touching
#      #
#      #    #############################################################################
#      #    # plot data sets
#      #
#      #    plt.plot(zgrid, nz,
#      #        color='black',
#      #        linestyle='-',              # -/--/-./:
#      #        linewidth=1,                # linewidth=1
#      #        marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
#      #        markerfacecolor='black',
#      #        markersize=0,               # markersize=6
#      #        label=r"data"               # '__nolegend__'
#      #        )
#      #
#      #    #############################################################################
#      #
#      #    # subplot data sets
#      #    ax1.set_xscale('linear')                     # ['linear' | 'log' | 'symlog']
#      #    ax1.set_yscale('linear')                     # ['linear' | 'log' | 'symlog']
#      #    # ax1.set_xlim(xmin=20.0,xmax=50.0)
#      #    # ax1.set_ylim(ymin=0.0,ymax=1800.0)
#      #
#      #    # subplot text sets
#      #    ax1.set_title('plot title', fontsize=16, fontweight="bold")  # fontsize=16
#      #    ax1.set_xlabel('x', fontsize=14, fontweight="bold")          # fontsize=12
#      #    ax1.set_ylabel('y', fontsize=14, fontweight="bold")          # fontsize=12
#      #
#      #    # legend
#      #    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
#      #    ax1.legend(loc=0, prop=prop, numpoints=1)
#      #
#      #    # # adding minor ticks
#      #    # xminorLocator = plt.MultipleLocator(0.01)           # minor ticks location in absolute units
#      #    # yminorLocator = plt.MultipleLocator(0.5)            # minor ticks location in absolute units
#      #    # # xminorLocator = plt.MaxNLocator(20)                 # set minor ticks number - can look weird
#      #    # # yminorLocator = plt.MaxNLocator(10)                 # set minor ticks number - can look weird
#      #    #
#      #    # ax1.xaxis.set_minor_locator(xminorLocator)
#      #    # ax1.yaxis.set_minor_locator(yminorLocator)
#      #
#      #    # x - axis tick labels
#      #    for label in ax1.xaxis.get_ticklabels():
#      #        label.set_color('black')
#      #        label.set_rotation(0)                   # default = 0
#      #        label.set_fontsize(14)                  # default = 12
#      #        label.set_fontweight("bold")            # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']
#      #
#      #    # y - axis tick labels
#      #    for label in ax1.yaxis.get_ticklabels():
#      #        label.set_color('black')
#      #        label.set_rotation(0)                   # default = 0
#      #        label.set_fontsize(14)                  # default = 12
#      #        label.set_fontweight("bold")            # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']
#      #
#      #    # save figure
#      #    plt.savefig(fig_name)
#      #
#      #
#      #    #############################################################################
#      #    # stop plot enviroment
#      #    #############################################################################
#      #
#      #
#      #
#      #
#      #    # from scipy.integrate import quad
#      #    # def integrand(t,n,x,norm):
#      #        # return norm*exp(-x*t) / t**n
#      #    #
#      #    # def expint(x,n, norm):
#      #        # return quad(integrand, 1, Inf, args=(n, x, norm))[0]
#      #    #
#      #    # result = quad(lambda x: expint(x,5), 0, inf)[0]
#      #    # print result
#
#
#

    ######################################################################
    # virial overdensity

    h_0=70.0
    omega_dm_0 = 0.25
    omega_b_0 = 0.05
    omega_m_0 = omega_dm_0 + omega_b_0
    omega_de_0 = 0.7
    omega_k_0 = 1.0 - omega_m_0 - omega_de_0
    sigma_8_0 = 0.8

    npoints=120

    z = linspace(0, 1.2, npoints)
    omega_m_z = zeros(npoints, dtype=float64)
    delta_vir = zeros(npoints, dtype=float64)


    for i in range(npoints):
        omega_m_z[i] = omega_m_z_func(z=z[i], h_0=h_0, omega_m_0=omega_m_0, omega_de_0=omega_de_0, omega_k_0=omega_k_0)
        delta_vir[i]=virial_overdensity(omega_m_z[i]) * omega_m_z[i] # result in mean matter density


    from pylab import rc
    import matplotlib.pyplot as plt
    import matplotlib.font_manager
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter, LogLocator

    ######################################################################
    # start plot enviroment
    ######################################################################
    # start figure
    rc('axes', linewidth=1.5)
    fig_obj = plt.figure()
    fig_name='delta_virial_z.png'
    headline_text = fig_obj.text(0.5, 0.95, '',
               horizontalalignment='center',
               fontproperties=matplotlib.font_manager.FontProperties(size=16))

    ax1 = fig_obj.add_subplot(111)                         # rows/cols/num of plot
    plt.subplots_adjust(hspace=0.2, wspace=0.2)      # hdefault 0.2, 0.001 for touching

    ######################################################################
    # plot data sets

    plt.plot(z, delta_vir,
             color='black',
             linestyle='-',              # -/--/-./:
                 linewidth=1,                # linewidth=1
             marker='',                  # ./o/*/+/x/^/</>/v/s/p/h/H
             markerfacecolor='black',
             markersize=0,               # markersize=6
             label=r"data"               # '__nolegend__'
             )

    plt.axhline(200.0, color="red")

    ######################################################################
    # subplot data sets
    ax1.set_xscale('linear')                     # ['linear' | 'log' | 'symlog']
    ax1.set_yscale('linear')                     # ['linear' | 'log' | 'symlog']
    # ax1.set_xlim(xmin=20.0,xmax=50.0)
    # ax1.set_ylim(ymin=20.0,ymax=50.0)

    # subplot text sets
    # ax1.set_title('plot title', fontsize=16, fontweight="bold")  # fontsize=16
    ax1.set_xlabel('z', fontsize=14, fontweight="bold")          # fontsize=12
    ax1.set_ylabel("$\delta$", fontsize=14, fontweight="bold")          # fontsize=12

    # legend
    prop = matplotlib.font_manager.FontProperties(size=16)  # size=16
    ax1.legend(loc=0, prop=prop, numpoints=1)

    # adding minor ticks
    # xminorLocator = plt.MultipleLocator(0.01)           # minor ticks location in absolute units
    # yminorLocator = plt.MultipleLocator(0.5)            # minor ticks location in absolute units
    # xminorLocator = plt.MaxNLocator(20)                 # set minor ticks number - can look weird
    # yminorLocator = plt.MaxNLocator(10)                 # set minor ticks number - can look weird

    # ax1.xaxis.set_minor_locator(xminorLocator)
    # ax1.yaxis.set_minor_locator(yminorLocator)

    # x - axis tick labels
    for label in ax1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("bold")            # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']

    # y - axis tick labels
    for label in ax1.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)                   # default = 0
        label.set_fontsize(14)                  # default = 12
        label.set_fontweight("bold")            # [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight']

    # save figure
    plt.savefig(fig_name)

    ######################################################################
    # stop plot enviroment
    ######################################################################

    print virial_overdensity(1.0)
    print omega_m_z
