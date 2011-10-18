######################################################################
# preliminary script for extraction of files for spectral analysis
# uses very standard and simple local bg approach
# requires double cleaned eventlist and defined extraction regions
# run it from /analysis and requires $ra and $de as input

dir=$1
here=`pwd`
cd $dir

specdir=../spec

######################################################################
# settings

ra=$2                           # until I am keeping it on github...
de=$3

EXTRACT_SRC=1
EXTRACT_BG=1

MAKE_RMF=1
MAKE_ARF=1
MAKE_BACKSCALE=1

SRC_REGION=cluster-man.phy.reg
BG_REGION=bg-ann-01.phy.reg
PS_REGION=ps-man.phy.reg


######################################################################
# create the spectroscopy dir if not existis

if [[ ! -e $specdir ]]
then
    mkdir ${specdir}
    mkdir ${specdir}/conf
    cp ${codedir}/template-par-qspec-001.conf ${specdir}/conf/
    cp ${codedir}/template-par-qspec-001.results ${specdir}/conf/
fi



######################################################################
# check existence of region files

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

if [[ $EXTRACT_SRC -ne 0 ]]
then

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
fi

if [[ $EXTRACT_BG -ne 0 ]]
then

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

fi


######################################################################
# GETTING RMF:

if [[ $MAKE_RMF -ne 0 ]]
then

    if [[ $EXTRACT_SRC -ne 0 ]]
    then

        echo -e '\nGetting source RMF...'
        rmfgen spectrumset=${specdir}/pn.pha rmfset=${specdir}/pn.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
        rmfgen spectrumset=${specdir}/m1.pha rmfset=${specdir}/m1.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
        rmfgen spectrumset=${specdir}/m2.pha rmfset=${specdir}/m2.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}

    fi


    if [[ $EXTRACT_BG -ne 0 ]]
    then

        echo -e '\nGetting background RMF...'
        rmfgen spectrumset=${specdir}/pn-${bgid}.pha rmfset=${specdir}/pn-${bgid}.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
        rmfgen spectrumset=${specdir}/m1-${bgid}.pha rmfset=${specdir}/m1-${bgid}.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}
        rmfgen spectrumset=${specdir}/m2-${bgid}.pha rmfset=${specdir}/m2-${bgid}.rmf detmaptype=flat  withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de}

    fi

fi

######################################################################
# GETTING ARF:

if [[ $MAKE_ARF -ne 0 ]]
then

# WITH VIG CORR!!!!!!!!!!!! -> special purpose  - if you use: 1. local bg & 2. zcolumn of spectra is "NO"
    export set="withsourcepos=yes sourcecoords="eqpos" sourcex=${ra} sourcey=${de} withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"
#export set="withsourcepos=yes sourcecoords="det" sourcex=3320.25 sourcey=8438.24 withrmfset=true withdetbounds=yes extendedsource=yes detmaptype=flat filterdss=no detxbins=10 detybins=10 modelee=N withbadpixcorr=N modeleffarea=Y modelquantumeff=Y modelfiltertrans=Y"

    if [[ $EXTRACT_SRC -ne 0 ]]
    then

        echo -e '\nGetting source ARFs...'

        arfgen spectrumset=${specdir}/pn.pha  $set rmfset=${specdir}/pn.rmf  arfset=${specdir}/pn.arf
        arfgen spectrumset=${specdir}/m1.pha  $set rmfset=${specdir}/m1.rmf  arfset=${specdir}/m1.arf
        arfgen spectrumset=${specdir}/m2.pha  $set rmfset=${specdir}/m2.rmf  arfset=${specdir}/m2.arf
    fi

    if [[ $EXTRACT_BG -ne 0 ]]
    then
        echo -e '\nGetting background ARFs...'

        arfgen spectrumset=${specdir}/pn-${bgid}.pha  $set rmfset=${specdir}/pn-${bgid}.rmf  arfset=${specdir}/pn-${bgid}.arf
        arfgen spectrumset=${specdir}/m1-${bgid}.pha  $set rmfset=${specdir}/m1-${bgid}.rmf  arfset=${specdir}/m1-${bgid}.arf
        arfgen spectrumset=${specdir}/m2-${bgid}.pha  $set rmfset=${specdir}/m2-${bgid}.rmf  arfset=${specdir}/m2-${bgid}.arf
    fi

fi


######################################################################
# backscale

if [[ $MAKE_BACKSCALE -ne 0 ]]
then

    if [[ $EXTRACT_SRC -ne 0 ]]
    then

        echo "Backscaling source spectra"

        prefix=$M1_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m1.pha badpixlocation=$evlist useodfatt=yes

        prefix=$M2_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m2.pha badpixlocation=$evlist useodfatt=yes

        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
        backscale spectrumset=${specdir}/pn.pha badpixlocation=$evlist useodfatt=yes

    fi


    if [[ $EXTRACT_BG -ne 0 ]]
    then

        echo "Backscaling background spectra"

        prefix=$M1_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m1-${bgid}.pha badpixlocation=$evlist useodfatt=yes

        prefix=$M2_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        backscale spectrumset=${specdir}/m2-${bgid}.pha badpixlocation=$evlist useodfatt=yes

        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
        backscale spectrumset=${specdir}/pn-${bgid}.pha badpixlocation=$evlist useodfatt=yes

    fi

fi


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
