######################################################################
# preliminary script to create a fitting session
#
# not completely functional - setup is OK, but might crash during
# fitting, needs xspec >v.12 and the diagonalized response matrices
# (.tar.gz, directly in /analysis)
#
# model based on Snowden & Kuntz, 2011 and Snowden et al., adapted from
# the esas .xcm file
#
# call (in /analysis): ./fitter.sh
# xspec < fitter.xspec
#

echo " querry yes


data 1:1 mos1S003-obj-full-grp.pi
data 2:2 mos2S004-obj-full-grp.pi
data 3:3 pnS005-obj-os-full-grp.pi
data 4:4 rass.pi

ignore 1:0.0-0.3,11.0-**
ignore 2:0.0-0.3,11.0-**
ignore 3:0.0-0.4,11.0-**
ig bad

response  2:1 mos1-diag.rsp.gz
response  3:2 mos2-diag.rsp.gz
response  4:3 pn-diag.rsp.gz

statistic chi
method leven 100 0.01
abund angr
xsect bcmc
cosmo 70 0 0.73
xset delta -1
systematic 0

cpd /xw
setplot energy


model  gaussian + gaussian + gaussian + gaussian + gaussian + gaussian + gaussian + constant*constant(gaussian + gaussian + gaussian + apec + (apec + apec + powerlaw)wabs + apec*wabs)
         1.4914      -0.05          0          0      1e+06      1e+06
      0.0075373      -0.05          0          0         10         20
    0.000280398       0.01          0          0      1e+24      1e+24
        1.74008      -0.05          0          0      1e+06      1e+06
    4.81313e-07      -0.05          0          0         10         20
    0.000105551       0.01          0          0      1e+24      1e+24
            7.1      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
              0      -0.01          0          0      1e+24      1e+24
            8.2      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
              0      -0.01          0          0      1e+24      1e+24
            8.5      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
              0      -0.01          0          0      1e+24      1e+24
            7.9      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
              0      -0.01          0          0      1e+24      1e+24
            7.5      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
              0      -0.01          0          0      1e+24      1e+24
        1.11639       0.01          0          0      1e+10      1e+10
        503.173      -0.01          0          0      1e+10      1e+10
           0.56      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
     3.8456e-07       0.01          0          0      1e+24      1e+24
           0.65      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
    2.23895e-07       0.01          0          0      1e+24      1e+24
        5.27384       0.05          0          0      1e+06      1e+06
        1.65701       0.05          0          0         10         20
    1.44753e-06       0.01          0          0      1e+24      1e+24
       0.100244       0.01      0.008      0.008         64         64
              1     -0.001          0          0          5          5
              0     -0.001          0          0          2          2
    3.01307e-06       0.01          0          0      1e+24      1e+24
            0.1      -0.01      0.008      0.008         64         64
              1     -0.001          0          0          5          5
              0     -0.001          0          0          2          2
              0      -0.01          0          0      1e+24      1e+24
       0.334597       0.01      0.008      0.008         64         64
              1     -0.001          0          0          5          5
              0     -0.001          0          0          2          2
    4.52486e-07       0.01          0          0      1e+24      1e+24
           1.46      -0.01         -3         -2          9         10
    8.33078e-07       0.01          0          0      1e+24      1e+24
          0.012     -0.001          0          0     100000      1e+06
        4.24611       0.01      0.008      0.008         64         64
        0.35508      0.001          0          0          5          5
      0.0615774      0.001          0          0          2          2
    0.000141942       0.01          0          0      1e+24      1e+24
= 47
= 1
= 2
    0.000293427       0.01          0          0      1e+24      1e+24
= 4
= 5
    0.000102397       0.01          0          0      1e+24      1e+24
= 7
= 8
= 9
= 10
= 11
= 12
= 13
= 14
= 15
= 16
= 17
= 18
= 19
= 20
= 21
              1      -0.01          0          0      1e+10      1e+10
        577.659      -0.01          0          0      1e+10      1e+10
= 24
= 25
= 26
= 27
= 28
= 29
= 30
= 31
= 32
= 33
= 34
= 35
= 36
= 37
= 38
= 39
= 40
= 41
= 42
= 43
= 44
= 45
= 46
= 47
= 48
= 49
= 50
= 51
= 52
        1.48448      -0.05          0          0      1e+06      1e+06
      0.0151104      -0.05          0          0         10         20
    5.90773e-05       0.01          0          0      1e+24      1e+24
= 4
= 5
              0      -0.01          0          0      1e+24      1e+24
        7.11089      -0.05          0          0      1e+06      1e+06
              0      -0.05          0          0         10         20
    1.30474e-05       0.01          0          0      1e+24      1e+24
        8.90831      -0.05          0          0      1e+06      1e+06
      0.0671747      -0.05          0          0         10         20
    0.000175454       0.01          0          0      1e+24      1e+24
        8.60897      -0.05          0          0      1e+06      1e+06
      0.0507249      -0.05          0          0         10         20
     0.00015841       0.01          0          0      1e+24      1e+24
         8.0435      -0.05          0          0      1e+06      1e+06
      0.0285638      -0.05          0          0         10         20
    0.000858717       0.01          0          0      1e+24      1e+24
        7.48298      -0.05          0          0      1e+06      1e+06
      0.0470736      -0.05          0          0         10         20
    0.000121409       0.01          0          0      1e+24      1e+24
       0.934904       0.01          0          0      1e+10      1e+10
        571.375      -0.01          0          0      1e+10      1e+10
= 24
= 25
= 26
= 27
= 28
= 29
= 30
= 31
= 32
= 33
= 34
= 35
= 36
= 37
= 38
= 39
= 40
= 41
= 42
= 43
= 44
= 45
= 46
= 47
= 48
= 49
= 50
= 51
= 52
= 1
= 2
              0      -0.01          0          0      1e+24      1e+24
= 4
= 5
              0      -0.01          0          0      1e+24      1e+24
= 7
= 8
              0      -0.01          0          0      1e+24      1e+24
= 10
= 11
= 12
= 13
= 14
= 15
= 16
= 17
= 18
= 19
= 20
= 21
              1      -0.01          0          0      1e+10      1e+10
              1      -0.01          0          0      1e+10      1e+10
= 24
= 25
              0      -0.01          0          0      1e+24      1e+24
= 27
= 28
              0      -0.01          0          0      1e+24      1e+24
= 30
= 31
              0      -0.01          0          0      1e+24      1e+24
= 33
= 34
= 35
= 36
= 37
= 38
= 39
= 40
= 41
= 42
= 43
= 44
= 45
= 46
= 47
= 48
= 49
= 50
              0      -0.01          0          0      1e+24      1e+24
= 52
model  2:myback1 bknpower
        0.97208       0.01         -3         -2          9         10
              3      -0.01         -3         -2          9         10
= myback1:1
       0.131099       0.01          0          0      1e+24      1e+24
model  3:myback2 bknpower
= myback1:1
= myback1:2
= myback1:3
       0.128477       0.01          0          0      1e+24      1e+24
model  4:myback3 bknpower
        1.53003       0.01         -3         -2          9         10
              3      -0.01         -3         -2          9         10
= myback3:1
       0.361532       0.01          0          0      1e+24      1e+24


log model-initial.log
show model
log none


######################################################################
# freeze pre-first fit

# a gaussian line (energy/width)
freeze 30
freeze 31

# cxb temperatures
freeze 33
freeze 37
freeze 41

# cluster parameters
freeze 48
freeze 49
freeze 50

log model-prefit.log
show model
log none


######################################################################
# fitting

fit
thaw 48
fit

# thaw 33
# thaw 41

# fit


log model-fit.log
show model
log none


 exit
 y
" > fitter.xspec