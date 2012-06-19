#!/bin/bash

machine=`uname`

# heasoft - sas11 conflict workaround
if [[ ${machine} == "Darwin" ]]
then
    export DYLD_LIBRARY_PATH=/Users/rs/data1/sw/heasoft-6.11/i386-apple-darwin10.7.0/lib
fi

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
# convert to ctr = cts/s

CONVERT_TO_CTR=0

if [[ $CONVERT_TO_CTR -eq 1 ]]
then

spec=inspec.pha

for i in m1-${bgid}.pha m2-${bgid}.pha m1-${SRC_REGION_ID}.pha m2-${SRC_REGION_ID}.pha # pn-${SRC_REGION_ID}.pha pn-{bgid}.pha
do
mv $i ${spec}
outspec=${i%.pha}.grp.pha

rm $outspec 2>/dev/null

mathpha <<EOT
${spec}
R
$i
$spec
1
0
EOT

rm ${spec}
done

# sleep 200

fi

######################################################################
# rebin the spectra

# background spectra
grppha infile=m1-${bgid}.pha outfile=m1-${bgid}.grp.pha chatter=0 comm=" group min ${m1_group_min} & chkey RESPFILE m1-${bgid}.rmf & chkey ANCRFILE m1-${bgid}.arf & chkey BACKFILE none & exit" clobber=yes
grppha infile=m2-${bgid}.pha outfile=m2-${bgid}.grp.pha chatter=0 comm=" group min ${m2_group_min} & chkey RESPFILE m2-${bgid}.rmf & chkey ANCRFILE m2-${bgid}.arf & chkey BACKFILE none & exit" clobber=yes
grppha infile=pn-${bgid}.pha outfile=pn-${bgid}.grp.pha chatter=0 comm=" group min ${pn_group_min} & chkey RESPFILE pn-${bgid}.rmf & chkey ANCRFILE pn-${bgid}.arf & chkey BACKFILE none & exit" clobber=yes

# source spectra
grppha infile=m1-${SRC_REGION_ID}.pha outfile=m1.grp.pha chatter=0 comm=" group min ${m1_group_min} & chkey RESPFILE m1-${SRC_REGION_ID}.rmf & chkey ANCRFILE m1-${SRC_REGION_ID}.arf & chkey BACKFILE m1-${bgid}.grp.pha & exit" clobber=yes
grppha infile=m2-${SRC_REGION_ID}.pha outfile=m2.grp.pha chatter=0 comm=" group min ${m2_group_min} & chkey RESPFILE m2-${SRC_REGION_ID}.rmf & chkey ANCRFILE m2-${SRC_REGION_ID}.arf & chkey BACKFILE m2-${bgid}.grp.pha & exit" clobber=yes
grppha infile=pn-${SRC_REGION_ID}.pha outfile=pn.grp.pha chatter=0 comm=" group min ${pn_group_min} & chkey RESPFILE pn-${SRC_REGION_ID}.rmf & chkey ANCRFILE pn-${SRC_REGION_ID}.arf & chkey BACKFILE pn-${bgid}.grp.pha & exit" clobber=yes

######################################################################
# hack header - grppha overwrites

CONVERT_TO_CTR=1
if [[ $CONVERT_TO_CTR -eq 1 ]]
then
echo "POISSERR=                    T / Poisson errors appropriate" > header.tmp
for i in pn-${bgid}.grp.pha pn.grp.pha # m1-${bgid}.grp.pha m2-${bgid}.grp.pha m1.grp.pha m2.grp.pha
do
    fmodhead $i header.tmp
done
rm header.tmp
# sleep 200
fi

######################################################################
# do the fitting
echo -e "
data 1:1 pn.grp.pha
data 2:2 m1.grp.pha
data 3:3 m2.grp.pha

cosmo 70 0 0.7

query yes
abund angr

setp e

ignore 1:1 0.0-$fit_band_min
ignore 1:1 $fit_band_max-**
ignore 2:2 0.0-$fit_band_min
ignore 2:2 $fit_band_max-**
ignore 3:3 0.0-$fit_band_min
ignore 3:3 $fit_band_max-**
ignore bad

model wabs(mekal)
$gal_nh
7.0
0.001
0.3
$redshift
1
0.01
=1
=2
=3
=4
=5
=6
=7
=1
=2
=3
=4
=5
=6
=7
freeze 1
freeze 3
freeze 4
freeze 2
untie 14 21

# cpd /xw
setplot rebin ${plot_bin_sigma} ${plot_bin_cts}
pl ld res

# weight standard
# weight model

statistic cstat
# statistic chi

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

iplot ldata res
time off

window 1
view .2 .4 .7 .9
la t
la y Normalised counts/s/keV

window 2
view .2 .1 .7 .4
la y Residuals
la t

csize 1.35
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
lumin 0.5 7.0 ${redshift}
log none

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

# abundance_err_d=`cat  ${spectrumid}-err.log | grep " 4 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
# abundance_err_u=`cat ${spectrumid}-err.log | grep " 4 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

abundance_err_d=NaN
abundance_err_u=NaN

# redshift_err_d=`cat   ${spectrumid}-err.log | grep " 5 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
# redshift_err_u=`cat  ${spectrumid}-err.log | grep " 5 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

redshift_err_d=NaN
redshift_err_u=NaN

normalisation_err_d=`cat   ${spectrumid}-err.log | grep " 7 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
normalisation_err_u=`cat  ${spectrumid}-err.log | grep " 7 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `


######################################################################
# write out report

echo
echo
echo "normalisation = "${normalisation_fit} ${normalisation_err_d} "+"${normalisation_err_u} | tee ${spectrumid}.result
echo "temperature = "${kt_fit} ${kt_err_d} "+"${kt_err_u} | tee -a ${spectrumid}.result
echo "redshift = "${redshift_fit} ${redshift_err_d} "+"${redshift_err_u} | tee -a ${spectrumid}.result
echo "Fe abundance = "${abundance_fit} ${abundance_err_d} "+"${abundance_err_u} | tee -a ${spectrumid}.result
echo
echo


######################################################################
# not used at the moment

terr=`calc \(${kt_err_u} + abs\(${kt_err_d}\)\)/2.0`
aerr=`calc \(${abundance_err_u} + abs\(${abundance_err_d}\)\)/2.0`
zerr=`calc \(${redshift_err_u} + abs\(${redshift_err_d}\)\)/2.0`

tsig=`calc ${kt_fit} / ${terr}`
asig=`calc ${abundance_fit} / ${aerr}`
zsig=`calc ${redshift_fit} / ${zerr}`

######################################################################
# plot conversions
convert -density 100 -alpha off -rotate 90 ${cluster}-${fitid}-nice.ps ${cluster}-${fitid}-nice.png

gather-quickspec-results.sh ${fitid}

echo "Spectroscopical analysis done for :" ${cluster} ${fitid}

