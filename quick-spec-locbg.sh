######################################################################
# preliminary script for extraction of files for spectral analysis
# uses very standard and simple local bg approach
# requires double cleaned eventlist and defined extraction regions

dir=$1
here=`pwd`
cd $dir

specdir=../spec


######################################################################
# set the region files: phys coords needed

SRC_REGION=cluster-man.phy.reg
BG_REGION=bg-ann-01.phy.reg
PS_REGION=ps.phy.reg


if [[ ! -e $SRC_REGION ]]
then
    echo -e "\n** error: $SRC_REGION does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

if [[ ! -e $BG_REGION ]]
then
    echo -e "\n** error: $BG_REGION does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

if [[ ! -e $PS_REGION ]]
then
    echo -e "\n** error: $PS_REGION does not exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

cp $SRC_REGION $BG_REGION $PS_REGION $specdir
bgid=`echo $BG_REGION | sed 's/\..*//g'`

######################################################################
# parse the region files, second parameter equals 0 means region file
# will be removed

parse-spec-reg.sh $SRC_REGION 1
parse-spec-reg.sh $BG_REGION 1
parse-spec-reg.sh $PS_REGION 0


######################################################################
# prepare the region descriptors

inpattern=`cat ${PS_REGION}.desc`
psreg="$inpattern"

inpattern=`cat ${SRC_REGION}.desc`
srcreg="$inpattern"

inpattern=`cat ${BG_REGION}.desc`
bgreg="$inpattern"


mospattern="#XMMEA_EM && ((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=12) && (PI in [100:10000])"
pnpattern="((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=4) && (PI in [100:10000])"


######################################################################
#  get m1 spectra

echo -e '\nGetting m1 spectra...'

mosexpr="$mospattern && $srcreg $psreg"
prefix=$M1_EV_PREFIX_LIST
evlist=mos${prefix}-clean.fits

evselect table=${evlist} withimageset=yes imageset=${specdir}/m1.im \
xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
withspectrumset=true spectrumset=${specdir}/m1.pha \
withspecranges=true energycolumn=PI specchannelmin=0 \
specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
writedss=Y expression="$mosexpr"



######################################################################
#  get m2 spectra

echo -e '\nGetting m2 spectra...'

mosexpr="$mospattern && $srcreg $psreg"
prefix=$M2_EV_PREFIX_LIST
evlist=mos${prefix}-clean.fits

evselect table=${evlist} withimageset=yes imageset=${specdir}/m2.im \
xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
withspectrumset=true spectrumset=${specdir}/m2.pha \
withspecranges=true energycolumn=PI specchannelmin=0 \
specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
writedss=Y expression="$mosexpr"



######################################################################
#  get pn spectra

echo -e '\nGetting pn spectra...'

pnexpr="$pnpattern && $srcreg $psreg"
prefix=$PN_EV_PREFIX_LIST
evlist=pn${prefix}-clean.fits

evselect table=${evlist} withimageset=yes imageset=${specdir}/pn.im \
xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
withspectrumset=true spectrumset=${specdir}/pn.pha \
withspecranges=true energycolumn=PI specchannelmin=0 \
specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
writedss=Y expression="$pnexpr"


######################################################################
#  get m1 background spectra

echo -e '\nGetting m1 background spectra...'

mosexpr="$mospattern && $bgreg $psreg"
prefix=$M1_EV_PREFIX_LIST
evlist=mos${prefix}-clean.fits

evselect table=${evlist} withimageset=yes imageset=${specdir}/m1-${bgid}.im \
xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
withspectrumset=true spectrumset=${specdir}/m1-${bgid}.pha \
withspecranges=true energycolumn=PI specchannelmin=0 \
specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
writedss=Y expression="$mosexpr"



######################################################################
#  get m2 background spectra

echo -e '\nGetting m2 background spectra...'

mosexpr="$mospattern && $bgreg $psreg"
prefix=$M2_EV_PREFIX_LIST
evlist=mos${prefix}-clean.fits

evselect table=${evlist} withimageset=yes imageset=${specdir}/m2-${bgid}.im \
xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
withspectrumset=true spectrumset=${specdir}/m2-${bgid}.pha \
withspecranges=true energycolumn=PI specchannelmin=0 \
specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
writedss=Y expression="$mosexpr"



######################################################################
#  get pn background spectra

echo -e '\nGetting pn background spectra...'

pnexpr="$pnpattern && $bgreg $psreg"
prefix=$PN_EV_PREFIX_LIST
evlist=pn${prefix}-clean.fits

evselect table=${evlist} withimageset=yes imageset=${specdir}/pn-${bgid}.im \
xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
withspectrumset=true spectrumset=${specdir}/pn-${bgid}.pha \
withspecranges=true energycolumn=PI specchannelmin=0 \
specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
writedss=Y expression="$pnexpr"


# if [[ $RMFARFRUN -gt 0 ]]
# then
# # GETTING RMF:
# echo -e '\nGetting RMFs...'

# rmfgen spectrumset=pn.pha rmfset=pn.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
# rmfgen spectrumset=m1.pha rmfset=m1.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
# rmfgen spectrumset=m2.pha rmfset=m2.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}

# rmfgen spectrumset=pn_locbg.pha rmfset=pn_locbg.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
# rmfgen spectrumset=m1_locbg.pha rmfset=m1_locbg.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
# rmfgen spectrumset=m2_locbg.pha rmfset=m2_locbg.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}



# # GETTING ARF:
# echo -e '\nGetting ARFs...'

# # WITH VIG CORR!!!!!!!!!!!! -> special purpose  - if you use: 1. local bg & 2. zcolumn of spectra is "NO"
# export set="withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"
# #export set="withsourcepos=yes sourcecoords="det" sourcex=3320.25 sourcey=8438.24 withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"
# arfgen spectrumset=pn.pha  $set rmfset=pn.rmf  arfset=pn.arf
# arfgen spectrumset=m1.pha  $set rmfset=m1.rmf  arfset=m1.arf
# arfgen spectrumset=m2.pha  $set rmfset=m2.rmf  arfset=m2.arf
# arfgen spectrumset=pn_locbg.pha  $set rmfset=pn_locbg.rmf  arfset=pn_locbg.arf
# arfgen spectrumset=m1_locbg.pha  $set rmfset=m1_locbg.rmf  arfset=m1_locbg.arf
# arfgen spectrumset=m2_locbg.pha  $set rmfset=m2_locbg.rmf  arfset=m2_locbg.arf



######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
