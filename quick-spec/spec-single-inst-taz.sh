#!/bin/bash

######################################################################
# load in setup

if [[ $# != 3 ]]
then
    echo -e "** error: missing clusterid, fitid and parameter file"
    echo -e "e.g.: ./spec-m1m2pn-ta.sh abc-0205 001 abc-0502-par-001.conf"
    exit 1
fi

cluster=$1
fitid=$2
parfile=$3

if [[ ! -e $parfile ]]
then
    echo -e "\n** error: $parfile does not exists here!"
    echo -e "*** error in $0\n"
    exit 1
fi

source $parfile

spectrumid=${cluster}-${fitid}

######################################################################
# rebin the spectra

# background spectra
grppha infile=m1-${bgid}.pha outfile=m1-${bgid}.grp.pha chatter=0 comm=" group min ${group_min} & chkey RESPFILE m1-${bgid}.rmf & chkey ANCRFILE m1-${bgid}.arf & chkey BACKFILE none & exit" clobber=yes

# source spectra
grppha infile=${single_inst}.pha outfile=${single_inst}.grp.pha chatter=0 comm=" group min ${group_min} & chkey RESPFILE ${single_inst}.rmf & chkey ANCRFILE ${single_inst}.arf & chkey BACKFILE m1-${bgid}.grp.pha & exit" clobber=yes


echo -e "
data 1:1 ${single_inst}.grp.pha

query yes
abund angr

setp e

ignore 1:1 0.-0.4
ignore 1:1 10.-**
ignore bad

model wabs(mekal)
$gal_nh
7.0
0.001
0.3
$redshift
1
0.01
freeze 1
freeze 3
freeze 4
freeze 2

# cpd /xw
setplot rebin ${plot_bin_sigma} ${plot_bin_cts}
pl ld res

# weight standard
# weight model

statistic cstat

fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
thaw 2
freeze 7
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
thaw 7
thaw 5
fit 100000000
fit 100000000
fit 100000000
fit 100000000
thaw 4
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000
fit 100000000

setplot rebin ${plot_bin_sigma} ${plot_bin_cts}
plot ldata

log ${cluster}-${fitid}-session.log
fit 20
log none
log ${cluster}-${fitid}-err.log
 error 1.0 2
 error 1.0 4
 error 1.0 5
 error 1.0 7
log none
log ${cluster}-${fitid}-gof.log
goodness ${nsim} nosim
goodness ${nsim} sim
log none

log ${cluster}-${fitid}-model.xcm
fit
log none
save ${cluster}-${fitid}-model.xcm

setplot rebin ${plot_bin_sigma} ${plot_bin_cts}
iplot ufspec
label f ${cluster}, xmm, ${fitid}
csize 1.3
lweigh 2
lab t
time off
hardcopy ${cluster}-${fitid}-uf.ps/cps
exit

plot ufspec

iplot ldata res
csize 1.3
lweigh 2
lab t
time off
hardcopy ${cluster}-${fitid}-data.ps/cps
exit

plot ldata res

#################################################
# Nice plot

iplot

ma 4 on 1
ma 4 on 3

ma 6 on 4
ma 6 on 6

ma 12 on 7
ma 12 on 9

view .1 .1 .6 .9
window 2
view .1 .1 .6

window 1
csiz 1.35
la t
la f
time off

la y Normalised counts/s/keV

window 2
la x Channel energy (keV)

lw 2
font roman
hard ${cluster}-${fitid}-nice.ps/cps
exit
#################################################

# write a flux/luminosity log
log ${cluster}-${fitid}-fx-lx.log
dummyrsp
flux 0.5 2
flux 2 10
flux 0.5 7.0
flux 1.1 7.0

newpar 1 0
cosmo 70 0 0.7
lumin 0.5 2.0 ${redshift}
lumin 2.0 10.0 ${redshift}
lumin 0.001 100.0 ${redshift}

exit
y
" > ${cluster}-${fitid}.xspec

xspec < ${cluster}-${fitid}.xspec




######################################################################
# extract spectroscopy results

kt_fit=`cat  ${spectrumid}-session.log | grep "2    2   mekal      kT" | awk '{print $7}' `
abundance_fit=`cat ${spectrumid}-session.log | grep "4    2   mekal      Abundanc" | awk '{print $6}' `
redshift_fit=`cat ${spectrumid}-session.log | grep "5    2   mekal      Redshift" | awk '{print $6}' `
normalisation_fit=`cat ${spectrumid}-session.log | grep "7    2   mekal      norm" | awk '{print $6}' `

kt_err_d=`cat   ${spectrumid}-err.log | grep " 2 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
kt_err_u=`cat  ${spectrumid}-err.log | grep " 2 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

abundance_err_d=`cat  ${spectrumid}-err.log | grep " 4 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
abundance_err_u=`cat ${spectrumid}-err.log | grep " 4 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

# abundance_err_d=NaN
# abundance_err_u=NaN

redshift_err_d=`cat   ${spectrumid}-err.log | grep " 5 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
redshift_err_u=`cat  ${spectrumid}-err.log | grep " 5 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

# redshift_err_d=NaN
# redshift_err_u=NaN

normalisation_err_d=`cat   ${spectrumid}-err.log | grep " 7 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
normalisation_err_u=`cat  ${spectrumid}-err.log | grep " 7 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `


######################################################################
# write out report

echo
echo
echo "normalisation = "${normalisation_fit} ${normalisation_err_d} "+"${normalisation_err_u} | tee -a ${spectrumid}.result
echo "temperature = "${kt_fit} ${kt_err_d} "+"${kt_err_u} | tee ${spectrumid}.result
echo "redshift = "${redshift_fit} ${redshift_err_d} "+"${redshift_err_u} | tee -a ${spectrumid}.result
echo "Fe abundance = "${abundance_fit} ${abundance_err_d} "+"${abundance_err_u} | tee -a ${spectrumid}.result
echo
echo


######################################################################
# not used at the moment

terr=`~/data1/sw/calc/calc-src.txt \(${kt_err_u} + abs\(${kt_err_d}\)\)/2.0`
aerr=`~/data1/sw/calc/calc-src.txt \(${abundance_err_u} + abs\(${abundance_err_d}\)\)/2.0`
zerr=`~/data1/sw/calc/calc-src.txt \(${redshift_err_u} + abs\(${redshift_err_d}\)\)/2.0`

tsig=`~/data1/sw/calc/calc-src.txt ${kt_fit} / ${terr}`
asig=`~/data1/sw/calc/calc-src.txt ${abundance_fit} / ${aerr}`
zsig=`~/data1/sw/calc/calc-src.txt ${redshift_fit} / ${zerr}`

echo "Spectroscopical analysis done for :" ${cluster} ${fitid}
