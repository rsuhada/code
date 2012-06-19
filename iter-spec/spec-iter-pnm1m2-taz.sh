#!/bin/bash

machine=`uname`

# heasoft vs. sas11 workaround
if [[ ${machine} == "Darwin" ]]
then
    export TMP_DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}
    export DYLD_LIBRARY_PATH=/Users/rs/data1/sw/heasoft-6.11/i386-apple-darwin10.7.0/lib
fi

######################################################################
# load in setup

cluster=$1
parfile=$2
spectrumid=$3
BG_REGION_ID=$4
group_min=$5

if [[ ! -e $parfile ]]
then
    echo -e "\n** error: $parfile does not exists here!"
    echo -e "*** error in $0\n"
    exit 1
fi

source $parfile

fileid=${cluster}-${spectrumid}

######################################################################
# convert to ctr = cts/s

CONVERT_TO_CTR=0

if [[ $CONVERT_TO_CTR -eq 1 ]]
then

spec=inspec.pha

for i in m1-${spectrumid}.pha m2-${spectrumid}.pha m1.pha m2.pha
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
grppha infile=m1-${BG_REGION_ID}.pha outfile=m1-${BG_REGION_ID}.grp.pha chatter=0 comm=" group min ${m1_group_min} & chkey RESPFILE m1-${BG_REGION_ID}.rmf & chkey ANCRFILE m1-${BG_REGION_ID}.arf & chkey BACKFILE none & exit" clobber=yes
grppha infile=m2-${BG_REGION_ID}.pha outfile=m2-${BG_REGION_ID}.grp.pha chatter=0 comm=" group min ${m2_group_min} & chkey RESPFILE m2-${BG_REGION_ID}.rmf & chkey ANCRFILE m2-${BG_REGION_ID}.arf & chkey BACKFILE none & exit" clobber=yes
grppha infile=pn-${BG_REGION_ID}.pha outfile=pn-${BG_REGION_ID}.grp.pha chatter=0 comm=" group min ${pn_group_min} & chkey RESPFILE pn-${BG_REGION_ID}.rmf & chkey ANCRFILE pn-${BG_REGION_ID}.arf & chkey BACKFILE none & exit" clobber=yes

# source spectra
grppha infile=m1-${spectrumid}.pha outfile=m1-${spectrumid}.grp.pha chatter=0 comm=" group min ${m1_group_min} & chkey RESPFILE m1-${spectrumid}.rmf & chkey ANCRFILE m1-${spectrumid}.arf & chkey BACKFILE m1-${BG_REGION_ID}.grp.pha & exit" clobber=yes
grppha infile=m2-${spectrumid}.pha outfile=m2-${spectrumid}.grp.pha chatter=0 comm=" group min ${m2_group_min} & chkey RESPFILE m2-${spectrumid}.rmf & chkey ANCRFILE m2-${spectrumid}.arf & chkey BACKFILE m2-${BG_REGION_ID}.grp.pha & exit" clobber=yes
grppha infile=pn-${spectrumid}.pha outfile=pn-${spectrumid}.grp.pha chatter=0 comm=" group min ${pn_group_min} & chkey RESPFILE pn-${spectrumid}.rmf & chkey ANCRFILE pn-${spectrumid}.arf & chkey BACKFILE pn-${BG_REGION_ID}.grp.pha & exit" clobber=yes

######################################################################
# hack header - grppha overwrites

CONVERT_TO_CTR=1

if [[ $CONVERT_TO_CTR -eq 1 ]]
then
echo "POISSERR=                    T / Poissonian errors applicable" > header.tmp
for i in pn-${bgid}.grp.pha pn-${spectrumid}.grp.pha # m1-${bgid}.grp.pha m2-${bgid}.grp.pha m1-${spectrumid}.grp.pha m2-${spectrumid}.grp.pha
do
    fmodhead $i header.tmp
done
rm header.tmp
fi

######################################################################
# do the fitting
echo -e "
data 1:1 pn-${spectrumid}.grp.pha
data 2:2 m1-${spectrumid}.grp.pha
data 3:3 m2-${spectrumid}.grp.pha

query yes
abund angr

setp e

ignore 1:1 0.-${fit_band_min}
ignore 1:1 ${fit_band_max}-**
ignore 2:2 0.-${fit_band_min}
ignore 2:2 ${fit_band_max}-**
ignore 3:3 0.-${fit_band_min}
ignore 3:3 ${fit_band_max}-**
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

# write a flux/luminosity log - abosrbed fx/lumin
log ${fileid}-fx-lx-err.log
# dummyrsp
flux 0.5 2 err 1000 68.2689
flux 2 10 err 1000 68.2689
flux 0.5 7.0 err 1000 68.2689
flux 1.1 7.0 err 1000 68.2689
lumin 0.5 2.0 ${redshift} err 1000 68.2689
lumin 2.0 10.0 ${redshift} err 1000 68.2689
lumin 0.001 100.0 ${redshift} err 1000 68.2689
lumin 0.5 7.0 ${redshift} err 1000 68.2689
log none

setplot rebin ${plot_bin_sigma} ${plot_bin_cts}
plot ldata

log ${fileid}-session.log
fit 20
log none
log ${fileid}-err.log
 error 1.0 2
 error 1.0 4
 error 1.0 5
 error 1.0 7
log none
log ${fileid}-gof.log
goodness ${nsim} nosim
goodness ${nsim} sim
log none

log ${fileid}-model.xcm
fit
log none
save ${fileid}-model.xcm

setplot rebin ${plot_bin_sigma} ${plot_bin_cts}
iplot ufspec
label f ${cluster}, xmm, ${spectrumid}
csize 1.3
lweigh 2
lab t
time off
hardcopy ${fileid}-uf.ps/cps
exit

plot ufspec

iplot ldata res
csize 1.3
lweigh 2
lab t
time off
hardcopy ${fileid}-data.ps/cps
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
hard ${fileid}-nice.ps/cps
exit
#################################################

log ${fileid}-fx-lx.log
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
" > ${fileid}.xspec

xspec < ${fileid}.xspec

######################################################################
# extract spectroscopy results

kt_fit=`cat  ${fileid}-session.log | grep "2    2   mekal      kT" | awk '{print $7}' `
abundance_fit=`cat ${fileid}-session.log | grep "4    2   mekal      Abundanc" | awk '{print $6}' `
redshift_fit=`cat ${fileid}-session.log | grep "5    2   mekal      Redshift" | awk '{print $6}' `
normalisation_fit=`cat ${fileid}-session.log | grep "7    2   mekal      norm" | awk '{print $6}' `

kt_err_d=`cat   ${fileid}-err.log | grep " 2 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
kt_err_u=`cat  ${fileid}-err.log | grep " 2 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

abundance_err_d=`cat  ${fileid}-err.log | grep " 4 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
abundance_err_u=`cat ${fileid}-err.log | grep " 4 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

redshift_err_d=`cat   ${fileid}-err.log | grep " 5 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
redshift_err_u=`cat  ${fileid}-err.log | grep " 5 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

normalisation_err_d=`cat   ${fileid}-err.log | grep " 7 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $5}' `
normalisation_err_u=`cat  ${fileid}-err.log | grep " 7 " | grep "(" | awk '{gsub("[(]",""); gsub("[)]",""); gsub(",","  "); print $6}' `

######################################################################
# write out report

echo
echo
echo "normalisation" ${normalisation_fit} ${normalisation_err_d} "+"${normalisation_err_u} | tee ${fileid}.result
echo "temperature" ${kt_fit} ${kt_err_d} "+"${kt_err_u} | tee -a ${fileid}.result
echo "redshift" ${redshift_fit} ${redshift_err_d} "+"${redshift_err_u} | tee -a ${fileid}.result
echo "abundance" ${abundance_fit} ${abundance_err_d} "+"${abundance_err_u} | tee -a ${fileid}.result
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
convert -density 100 -alpha off -rotate 90 ${fileid}-nice.ps ${fileid}-nice.png

echo "Spectroscopical analysis done for :" ${cluster} ${spectrumid}

# reinstate sas11 DYLD path
if [[ ${machine} == "Darwin" ]]
then
    # export DYLD_LIBRARY_PATH=/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803/libsys:/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803/libextra:/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803/lib:/Users/rs/data1/sw/heasoft-6.11/i386-apple-darwin10.7.0/lib
    export DYLD_LIBRARY_PATH=${TMP_DYLD_LIBRARY_PATH}
fi