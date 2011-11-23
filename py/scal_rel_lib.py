#!/usr/bin/env python
import math
from numpy import *


#############################################################################################
### L-T scalings

def LT_markevitch98(luminosity, func_ez):
    """
    # INPUT: luminosity 0.1-2.4 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: version for excised cores
    """

    outT = 6.0*10**((math.log10(luminosity/func_ez) - 2.45)/2.1)
    return outT

def LT_markevitch98_err(luminosity, luminosity_err, func_ez):
    """
    # INPUT: luminosity 0.1-2.4 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: version for excised cores
    """

    outT = 6.0*10**((math.log10(luminosity/func_ez) - 2.45)/2.1)

    outT_err = outT * 6.0 * luminosity_err / (2.1* luminosity)
    return outT_err

###

def LT_gwp09(luminosity, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: BCSE orthogonal, no excision
    """

    outT = 5.0*(func_ez**(-1.0)*luminosity/(2.14*1.0e2))**(1.0/3.01)
    return outT

def LT_gwp09_err(luminosity, luminosity_err, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: BCSE orthogonal, no excision
    """

    ADD_INTRINSIC = 1
    INTRINSIC_SIGMA = 0.286             # in fraction, i.e. 0.286 -> 28.6% scatter

    outT = 5.0*(func_ez**(-1.0)*luminosity/(2.14*1.0e2))**(1.0/3.01)
    outT_err = outT*luminosity_err/(3.01*luminosity)

    if (ADD_INTRINSIC  ==  1):
        outT_intr_err =  INTRINSIC_SIGMA*outT
        outT_err = sqrt(outT_err**2.0 + outT_intr_err**2.0)


    return outT_err

def LT_gwp09_bol(luminosity_bol, func_ez):
    """
    # INPUT: luminosity bolometric inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: BCSE orthogonal, no excision
    """

    outT = 5.0*(func_ez**(-1.0)*luminosity_bol/(7.13*1.0e2))**(1.0/3.35)
    return outT

def LT_gwp09_bol_err(luminosity_bol, luminosity_bol_err, func_ez):
    """
    # INPUT: luminosity_bol 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: BCSE orthogonal, no excision
    """

    ADD_INTRINSIC = 1
    # INTRINSIC_SIGMA = 0.2446             # [bolo] in fraction, i.e. 0.286 -> 28.6% scatter
    INTRINSIC_SIGMA = 0.286              # [0.5-2] in fraction, i.e. 0.286 -> 28.6% scatter

    outT = 5.0*(func_ez**(-1.0)*luminosity_bol/(7.13*1.0e2))**(1.0/3.35)
    outT_err = outT*luminosity_bol_err/(3.35*luminosity_bol)

    if (ADD_INTRINSIC  ==  1):
        outT_intr_err =  INTRINSIC_SIGMA*outT
        outT_err = sqrt(outT_err**2.0 + outT_intr_err**2.0)


    return outT_err


#############################################################################################
### L-M scalings

def LM_gwp09(luminosity, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    #       func_ez**(-7.0/3.0) - paper has this but apparently its a mistake
    #       and should be -2, see email from gwp, fit in gwp09 is now
    #       likely inconsistent...
    """

    #outM = 20.0*(func_ez**(-7.0/3.0)*luminosity/(0.61*1.0e2))**(1.0/1.72)
    outM = 20.0*(func_ez**(-2.0)*luminosity/(0.61*1.0e2))**(1.0/1.72)

    return outM

def LM_gwp09_err(luminosity, luminosity_err, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    #       func_ez**(-7.0/3.0) - paper has this but apparently its a mistake
    #       and should be -2, see email from gwp, fit in gwp09 is now
    #       likely inconsistent...
    """

    ADD_INTRINSIC = 1
    INTRINSIC_SIGMA = 0.272             # in fraction, i.e. 0.286 -> 28.6% scatter

    #outM = 20.0*(func_ez**(-7.0/3.0)*luminosity/(0.61*1.0e2))**(1.0/1.72)
    outM = 20.0*(func_ez**(-2.0)*luminosity/(0.61*1.0e2))**(1.0/1.72)
    outM_err = outM*luminosity_err/(1.72*luminosity)

    if (ADD_INTRINSIC  ==  1):
        outM_intr_err =  INTRINSIC_SIGMA*outM
        outM_err = sqrt(outM_err**2.0 + outM_intr_err**2.0)


    return outM_err

def LM_gwp09_bol(luminosity_bol, func_ez):
    """
    # INPUT: luminosity boloetric  band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: BCSE orthogonal, no excision, yes malmquist bias correction
    # no-evol as given by fassbender10 (x1230 paper)
    """


    outM = 20.0*(func_ez**(-7.0/3.0)*luminosity_bol/(1.38*1.0e2))**(1.0/2.08)

    return outM

def LM_gwp09_bol_err(luminosity_bol, luminosity_bol_err, func_ez):
    """
    # INPUT: luminosity_bol 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: BCSE orthogonal, no excision, yes malmquist bias correction
    """


    ADD_INTRINSIC = 1
    # INTRINSIC_SIGMA = 0.2022             # [bolo] in fraction, i.e. 0.286 -> 28.6% scatter
    INTRINSIC_SIGMA = 0.272             # [0.5-2] in fraction, i.e. 0.286 -> 28.6% scatter

    outM = 20.0*(func_ez**(-7.0/3.0)*luminosity_bol/(1.38*1.0e2))**(1.0/2.08)
    outM_err = outM*luminosity_bol_err/(2.08*luminosity_bol)

    if (ADD_INTRINSIC  ==  1):
        outM_intr_err =  INTRINSIC_SIGMA*outM
        outM_err = sqrt(outM_err**2.0 + outM_intr_err**2.0)


    return outM_err

def LM_vikhlinin09(luminosity, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: h=70 hardwired atm
    """

    outM = (math.log(luminosity) + 42.0*math.log(10.0) - 47.392 - 1.85*math.log(func_ez) + 0.39*math.log(70.0/72.0) ) / 1.61
    outM = exp(outM - 13.0*math.log(10.0))

    return outM

def LM_vikhlinin09_err(luminosity, luminosity_err, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: h=70 hardwired atm
    """

    ADD_INTRINSIC = 1
    INTRINSIC_SIGMA = 0.279  # this is at fixed lumin, at fixed mass its 48% - agreeing with what vikhlinin writes


    outM = (math.log(luminosity) + 42.0*math.log(10.0) - 47.392 - 1.85*math.log(func_ez) + 0.39*math.log(70.0/72.0) ) / 1.61
    outM = exp(outM - 13.0*math.log(10.0))

    outM_err = outM*luminosity_err/(1.61*luminosity)

    if (ADD_INTRINSIC  ==  1):
        outM_intr_err =  INTRINSIC_SIGMA*outM
        outM_err = sqrt(outM_err**2.0 + outM_intr_err**2.0)


    return outM_err


#############################################################################################
# no-evol as given by fassbender10 (x1230 paper)

def LT_gwp09_bol_noevol(luminosity_bol, func_ez):
    """
    # INPUT: luminosity bolometric inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: BCSE orthogonal, no excision
    """

    outT = 5.0*(func_ez**(0.0)*luminosity_bol/(7.13*1.0e2))**(1.0/3.35)
    return outT

def LT_gwp09_bol_noevol_err(luminosity_bol, luminosity_bol_err, func_ez):
    """
    # INPUT: luminosity_bol 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: T [keV]
    # NOTE: BCSE orthogonal, no excision
    """

    ADD_INTRINSIC = 1
    # INTRINSIC_SIGMA = 0.2446             # [bolo] in fraction, i.e. 0.286 -> 28.6% scatter
    INTRINSIC_SIGMA = 0.286              # [0.5-2] in fraction, i.e. 0.286 -> 28.6% scatter

    outT = 5.0*(func_ez**(0.0)*luminosity_bol/(7.13*1.0e2))**(1.0/3.35)
    outT_err = outT*luminosity_bol_err/(3.35*luminosity_bol)

    if (ADD_INTRINSIC  ==  1):
        outT_intr_err =  INTRINSIC_SIGMA*outT
        outT_err = sqrt(outT_err**2.0 + outT_intr_err**2.0)


    return outT_err


def LM_gwp09_bol_noevol(luminosity_bol, func_ez):
    """
    # INPUT: luminosity boloetric  band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: BCSE orthogonal, no excision, yes malmquist bias correction
    # no-evol as given by fassbender10 (x1230 paper)
    """


    outM = 20.0*(func_ez**(-4.0/3.0)*luminosity_bol/(1.38*1.0e2))**(1.0/2.08)

    return outM

def LM_gwp09_bol_noevol_err(luminosity_bol, luminosity_bol_err, func_ez):
    """
    # INPUT: luminosity_bol 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: M [10**13 Msol]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    #       func_ez**(-7.0/3.0) - paper has this but apparently its a mistake
    #       and should be -2, see email from gwp, fit in gwp09 is now
    #       likely inconsistent...
    """

    ADD_INTRINSIC = 1
    # INTRINSIC_SIGMA = 0.2022             # [bolo] in fraction, i.e. 0.286 -> 28.6% scatter
    INTRINSIC_SIGMA = 0.272             # [0.5-2] in fraction, i.e. 0.286 -> 28.6% scatter

    outM = 20.0*(func_ez**(-4.0/3.0)*luminosity_bol/(1.38*1.0e2))**(1.0/2.08)
    outM_err = outM*luminosity_bol_err/(2.08*luminosity_bol)

    if (ADD_INTRINSIC  ==  1):
        outM_intr_err =  INTRINSIC_SIGMA*outM
        outM_err = sqrt(outM_err**2.0 + outM_intr_err**2.0)


    return outM_err





#############################################################################################
# M-T scalings

def MT_vikhlinin09(temperature, temperature_err, func_ez, h):
    """
    Arguments:
    - `temperature`: [keV] 0.15-1 r500 X-ray temperature
    - `temperature_err`: [keV] 0.15-1 r500 X-ray temperature error
    - `func_ez`: E = E(z) - the Hubble parameter evolution function
    - `h`: h = H(z=0)/100.0
    """
    M0 = 3.02e14/h
    alpha = 1.53

    outM = M0*(temperature/5.0)**alpha / func_ez

    # FIXME: error propagation
    outM_err = 999.0

    return (outM, outM_err)



def MT_finoguenov01(temperature, func_ez):
    """
    # INPUT: T inside r500, [keV]
    #         ez
    # OUTPUT: M [10**13 Msol]
    """

    outM = (2.36*temperature**1.89)/func_ez
    return outM

def MT_finoguenov01_err(temperature, temperature_err, func_ez):
    """
    # INPUT: T inside r500, [keV]
    #         ez
    # OUTPUT: M [10**13 Msol]
    """

    outM = (2.36*temperature**1.89)/func_ez

    outM_err = outM*1.89*temperature_err/temperature
    return outM_err

###

def MT_arnaud05(temperature, func_ez):
    """
    # INPUT: T inside r200, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: M500 [10**13 Msol]
    """

    # using coefficients for overdensity=500, T>2keV
    A = 3.84 * 10.0          # 10**13 Msol
    alpha = 1.71

    # using coefficients for overdensity=500, T>3.5keV
#    A = 4.10 * 10.0          # 10**13 Msol
#    alpha = 1.49

    outM = A*((temperature/5.0)**alpha)/func_ez
    return outM

def MT_arnaud05_err(temperature, temperature_err, func_ez):
    """
    # INPUT: T inside r200, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: M500 [10**13 Msol]
    """

    # using coefficients for overdensity=500, T>2keV
    A = 3.84 * 10.0          # 10**13 Msol
    alpha = 1.71

    # using coefficients for overdensity=500, T>3.5keV
#    A = 4.10 * 10.0          # 10**13 Msol
#    alpha = 1.49

    outM = A*((temperature/5.0)**alpha)/func_ez

    outM_err = outM*alpha*temperature_err/temperature
    return outM_err

###

def M200T_arnaud05(temperature, func_ez):
    """
    # INPUT: T inside r200, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: M200 [10**13 Msol]
    """

    # using coefficients for overdensity=200, T>2keV
    A = 5.34 * 10.0          # 10**13 Msol
    alpha = 1.72

    # using coefficients for overdensity=200, T>3.5keV
#    A = 5.74 * 10.0          # 10**13 Msol
#    alpha = 1.49

    outM = A*((temperature/5.0)**alpha)/func_ez
    return outM

def M200T_arnaud05_err(temperature, temperature_err, func_ez):
    """
    # INPUT: T inside r200, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: M200 [10**13 Msol]
    """

    ADD_INTRINSIC = 1

    # using coefficients for overdensity=200, T>2keV
    A = 5.34 * 10.0          # 10**13 Msol
    alpha = 1.72
    INTRINSIC_SIGMA = 0.125

    # using coefficients for overdensity=200, T>3.5keV
#    A = 5.74 * 10.0          # 10**13 Msol
#    alpha = 1.49
#    INTRINSIC_SIGMA = 0.159

    outM = A*((temperature/5.0)**alpha)/func_ez
    outM_err = outM*alpha*temperature_err/temperature

    if (ADD_INTRINSIC  ==  1):
        outM_intr_err =  INTRINSIC_SIGMA*outM
        outM_err = sqrt(outM_err**2.0 + outM_intr_err**2.0)



    return outM_err

######################################################################
# T-T relations

def TT_vikhlinin09(temperature, temperature_err):
    """
    0.5r500 to r500 scaling of Vikhlinin+09.
    iscatter at <3% on the T/T2 ratio (negligible).

    Arguments:
    - `temperature`: 0.15-0.5 r500 temperature (T2)
    - `temperature_err`: 0.15-0.5 r500 temperature_err

    Output:
    - temperature in 0.15-1 r500 (T)
    - temperature error in 0.15-1 r500
    """

    ADD_INTRINSIC = 0
    a = 0.9075
    b = 0.00625


    outT = temperature * (a + b * temperature)
    outT_err = sqrt(a**2 * temperature_err**2 + (2.0*b*temperature*temperature_err)**2)

    if (ADD_INTRINSIC == 1):
        outT_intr_err = 0.03 * temperature # 3% iscatter on the T/T2 ratio
        outT_err = sqrt(outT_err**2 + outT_intr_err**2)

    return (outT, outT_err)


#############################################################################################
# r-T scalings

def RT_finoguenov01(temperature, func_ez):
    """
    # INPUT: T inside r500, [keV]
    #         ez
    # OUTPUT: r500 [Mpc]
    """

    outR = (0.391*temperature**0.63)/func_ez
    return outR

def RT_finoguenov01_err(temperature, temperature_err, func_ez):
    """
    # INPUT: T inside r500, [keV]
    #         ez
    # OUTPUT: r500 [Mpc]
    """

    outR = (0.391*temperature**0.63)/func_ez

    outR_err = 0.63*outR*temperature_err/temperature
    return outR_err

###

def RT_arnaud05(temperature, func_ez):
    """
    # INPUT: T inside r500, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: r500 [Mpc]
    """

    # coefficients for overdensity=500, T>2keV
    A = 1104.0 * 1.0e-3          # Mpc
    alpha = 0.57

    # coefficients for overdensity=500, T>3.5keV
#    A = 1129.0 * 1.0e-3          # Mpc
#    alpha = 0.50

    outR = A*((temperature/5.0)**alpha)/func_ez
    return outR


def RT_arnaud05_err(temperature, temperature_err, func_ez):
    """
    # INPUT: T inside r500, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: r500 [Mpc]
    """

    # coefficients for overdensity=500, T>2keV
    A = 1104.0 * 1.0e-3          # Mpc
    alpha = 0.57

    # coefficients for overdensity=500, T>3.5keV
#    A = 1129.0 * 1.0e-3          # Mpc
#    alpha = 0.50

    outR = A*((temperature/5.0)**alpha)/func_ez

    outR_err = outR*alpha*temperature_err/temperature
    return outR_err

###

def R200T_arnaud05(temperature, func_ez):
    """
    # INPUT: T inside r200, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: r200 [Mpc]
    """

    # coefficients for overdensity=200, T>2keV
    A = 1674.0 * 1.0e-3          # Mpc
    alpha = 0.57

    # coefficients for overdensity=200, T>3.5keV
#     A = 1714.0 * 1.0e-3          # Mpc
#     alpha = 0.50

    outR = A*((temperature/5.0)**alpha)/func_ez
    return outR

def R200T_arnaud05_err(temperature, temperature_err, func_ez):
    """
    # INPUT: T inside r200, [keV] - actually an overall [0.1-0.5]r200 T
    #         ez
    # OUTPUT: r200 [Mpc]
    """

    # coefficients for overdensity=200, T>2keV
    A = 1674.0 * 1.0e-3          # Mpc
    alpha = 0.57

    # coefficients for overdensity=200, T>3.5keV
#    A = 1714.0 * 1.0e-3          # Mpc
#    alpha = 0.50

    outR = A*((temperature/5.0)**alpha)/func_ez

    outR_err = outR*alpha*temperature_err/temperature
    return outR_err


#############################################################################################
# r-M exact analytic calculation

def r_overdensity(overdensity, mass, mass_err, func_ez):
    """
    # INPUT: M inside r_overrdensity
    #         ez
    # OUTPUT: r_overdensity [Mpc]
    """

    rho_crit= 1.139e12      # in Msol/Mpc**3
    rho_crit = rho_crit*3.0*(func_ez**2.0)/(8.0*math.pi)

    outR = (3.0*mass/(4.0*math.pi*rho_crit*overdensity))**(1.0/3.0)

    outR_err = outR*mass_err/(3.0*mass)
    return (outR, outR_err)


#############################################################################################
# M-Yx scalings

def MYx_arnaud07(mass, func_ez):
    """
    # INPUT: M inside r500, [1e13 Msol]
    #         ez
    # OUTPUT: Yx [10**13Msol keV]
    """

    # outY = 20.0*10**((math.log10(mass*func_ez**(2.0/5.0)) + 13.0 - 14.556)/0.548)

    normalization=10**(14.556-13.0)
    alpha = 0.548

    outY = 20.0*(func_ez**(2.0/5.0)*mass/normalization)**(1.0/alpha)
    return outY

def MYx_arnaud07_err(mass, mass_err, func_ez):
    """
    # INPUT: M inside r500, [1e13 Msol]
    #         ez
    # OUTPUT: Yx [10**13Msol keV]
    """

    #outY = 20.0*10**((math.log10(mass*func_ez**(2.0/5.0)) + 13.0 - 14.556)/0.548)
    #outY_err = 20.0*outY*mass_err/(0.548*mass)

    normalization=10**(14.556-13.0)
    alpha = 0.548

    outY = 20.0*(func_ez**(2.0/5.0)*mass/normalization)**(1.0/alpha)
    outY_err = outY*mass_err*(1.0/alpha)/mass
    return outY_err

#############################################################################################
### L-Yx scalings

def LY_gwp09(luminosity, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: Y [10**13 Msol keV]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    """

    outY = 20.0*(func_ez**(-9.0/5.0)*luminosity/(1.61*1.0e2))**(1.0/0.90)

    return outY

def LY_gwp09_err(luminosity, luminosity_err, func_ez):
    """
    # INPUT: luminosity 0.5-2.0 keV band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: Y [10**13 Msol keV]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    """

    ADD_INTRINSIC = 1
    INTRINSIC_SIGMA = 0.584        # in fraction, i.e. 0.286 -> 28.6% scatter

    outY = 20.0*(func_ez**(-9.0/5.0)*luminosity/(1.61*1.0e2))**(1.0/0.90)
    outY_err = outY*luminosity_err/(0.90*luminosity)

    if (ADD_INTRINSIC  ==  1):
        outY_intr_err =  INTRINSIC_SIGMA*outY
        outY_err = sqrt(outY_err**2.0 + outY_intr_err**2.0)


    return outY_err


def LY_gwp09_bol(luminosity, func_ez):
    """
    # INPUT: luminosity bolometric band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: Y [10**13 Msol keV]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    """

    outY = 20.0*(func_ez**(-9.0/5.0)*luminosity/(5.35*1.0e2))**(1.0/1.04)

    return outY

def LY_gwp09_bol_err(luminosity, luminosity_err, func_ez):
    """
    # INPUT: luminosity bolometric band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: Y [10**13 Msol keV]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    """

    ADD_INTRINSIC = 1
    # INTRINSIC_SIGMA = 0.44523      # [0.5-2] in fraction, i.e. 0.286 -> 28.6% scatter 0.383/2.08)
    INTRINSIC_SIGMA = 0.584        # [bolo] in fraction, i.e. 0.286 -> 28.6% scatter

    outY = 20.0*(func_ez**(-9.0/5.0)*luminosity/(5.35*1.0e2))**(1.0/1.04)
    outY_err = outY*luminosity_err/(0.90*luminosity)

    if (ADD_INTRINSIC  ==  1):
        outY_intr_err =  INTRINSIC_SIGMA*outY
        outY_err = sqrt(outY_err**2.0 + outY_intr_err**2.0)


    return outY_err


def LY_gwp09_bol_noevol(luminosity, func_ez):
    """
    # INPUT: luminosity bolometric band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: Y [10**13 Msol keV]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    # no evol pro forma
    """

    outY = 20.0*(func_ez**(-4.0/5.0)*luminosity/(5.35*1.0e2))**(1.0/1.04)

    return outY

def LY_gwp09_bol_noevol_err(luminosity, luminosity_err, func_ez):
    """
    # INPUT: luminosity bolometric band inside r500, [10**42 erg s-1]
    #         ez
    # OUTPUT: Y [10**13 Msol keV]
    # NOTE: BCSE orthogonal, no excision, no malmquist bias correction
    # no evol pro forma
    """

    ADD_INTRINSIC = 1
    # INTRINSIC_SIGMA = 0.44523      # [0.5-2] in fraction, i.e. 0.286 -> 28.6% scatter 0.383/2.08)
    INTRINSIC_SIGMA = 0.584        # [bolo] in fraction, i.e. 0.286 -> 28.6% scatter

    outY = 20.0*(func_ez**(-4.0/5.0)*luminosity/(5.35*1.0e2))**(1.0/1.04)
    outY_err = outY*luminosity_err/(0.90*luminosity)

    if (ADD_INTRINSIC  ==  1):
        outY_intr_err =  INTRINSIC_SIGMA*outY
        outY_err = sqrt(outY_err**2.0 + outY_intr_err**2.0)


    return outY_err


#############################################################################################
### SPT scalings

def spt_zeta(m500c, redshift):
    """
    # converts m500critical -> m200mean (through simple fit) -> spt zeta (ideal S/N)
    """

    # 1. convert to m500c to m200m
    a =  0.550202565078
    b =  -0.0155242264849
    m200m = (m500c - b)/a

    # m200m to zeta scaling
    #A = 6.01 # gaussian priors
    #B = 1.31 # gaussian priors
    #C = 1.60 # gaussian priors

    A = 5.17 # WMAP7+BAO+SN+SPT
    B = 1.43 # WMAP7+BAO+SN+SPT
    C = 1.38 # WMAP7+BAO+SN+SPT
    out_zeta = A * (0.7*m200m/50.0)**B * ((1+redshift)/1.6)**C        # check the h!
    return out_zeta

def spt_xi(zeta):
    """
    """

    out_xi = sqrt(zeta**2.0 + 3.0)
    return out_xi





if __name__ == '__main__':
    """
    Cluster scaling relation library.
    Based on the param.pro IDL script. Translation in progress.
    """

# FIXME: keep only scaling relations with errors, return tuples, check inputs
# FIXME: check the cosmological dependence - is everything isolated in Ez (should be, but check)


######################################################################
# list of refactored scaling relations

# MT_vikhlinin09 (needs error propagation)
# TT_vikhlinin09
# r_overdensity

