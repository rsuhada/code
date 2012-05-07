######################################################################
# extract full band spectrum and control image for the input
# instrument, within the input region and optionally provide also a
# point source exclusion file

source ${codedir}/utils/util-funcs-lib.sh

######################################################################
# inputs

instrument=$1
SRC_REGION=$2
spectrumid=$3
specdir=$4
PS_REGION=$5
CORE_REGION=$6

######################################################################
# parse the region files, second parameter equals 0 means region file
# will be removed, prepare the region descriptors

ds9reg_to_sasdesc $SRC_REGION 1
inpattern=`cat ${SRC_REGION}.desc`
srcreg="$inpattern"

if [[ $# -lt 5 ]]
then
    echo -e "No point source region file provided"
    psreg=""
else
    ds9reg_to_sasdesc $PS_REGION 0
    inpattern=`cat ${PS_REGION}.desc`
    psreg="$inpattern"

    if [[ $# -eq 6 ]]
    then
        ds9reg_to_sasdesc $CORE_REGION 0
        inpattern=`cat ${CORE_REGION}.desc`
        psreg="$psreg $inpattern"
    fi
fi

######################################################################
# select the eventlist and the selection pattern

case $instrument in
    "pn")
        instpattern="((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=4) && (PI in [100:10000])"
        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
        ootevlist=pn${prefix}-clean-oot.fits
        ;;
    "m1")
        instpattern="#XMMEA_EM && ((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=12) && (PI in [100:10000])"
        prefix=$M1_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        ;;
    "m2")
        instpattern="#XMMEA_EM && ((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=12) && (PI in [100:10000])"
        prefix=$M2_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        ;;
    *)
        echo "unknown instrument!"
        exit 1
esac

######################################################################
#  get source spectra

echo -e "\nGetting spectra for " $instrument

expr="$instpattern && $srcreg $psreg"

# XMM-BCS type binning
# evselect table=${evlist} withimageset=yes imageset=${specdir}/${instrument}-${spectrumid}.im \
#     xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
#     yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
#     withspectrumset=true spectrumset=${specdir}/${instrument}-${spectrumid}.pha \
#     withspecranges=true energycolumn=PI specchannelmin=0 \
#     specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
#     writedss=Y expression="$expr"

# ESAS type binning
evselect table=${evlist} withimageset=yes imageset=${specdir}/${instrument}-${spectrumid}.im \
    xcolumn=X ycolumn=Y withzcolumn=N withzerrorcolumn=N \
    ximagebinsize=1 yimagebinsize=1 squarepixels=yes \
    ximagesize=900 yimagesize=900 imagebinning=imageSize \
    withxranges=yes ximagemin=3401 ximagemax=48400 withxranges=yes \
    withyranges=yes yimagemin=3401 yimagemax=48400 withyranges=yes \
    withspectrumset=true spectrumset=${specdir}/${instrument}-${spectrumid}.pha \
    withspecranges=true energycolumn=PI specchannelmin=0 \
    specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
    writedss=Y expression="$expr"


# ESAS type binning - detection coords
evselect table=${evlist} withimageset=yes imageset=${specdir}/${instrument}-${spectrumid}-detmap.ds \
    xcolumn=DETX ycolumn=DETY withzcolumn=N withzerrorcolumn=N \
    ximagebinsize=1 yimagebinsize=1 squarepixels=yes \
    ximagesize=900 yimagesize=900 imagebinning=imageSize \
    withspectrumset=false spectrumset=${specdir}/${instrument}-${spectrumid}.pha \
    withspecranges=true energycolumn=PI specchannelmin=0 \
    specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
    writedss=Y expression="$expr"


######################################################################
# if pn create also the oot stuff

if [[ "$instrument" == "pn" ]]
then

    ######################################################################
    # extract oot

    echo "extracting oot spectra for $instrument!"
    expr="$instpattern && $srcreg $psreg"

    # XMM-BCS type binning
    # evselect table=${ootevlist} withimageset=yes imageset=${specdir}/${instrument}-${spectrumid}-oot.im \
    #     xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
    #     yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
    #     withspectrumset=true spectrumset=${specdir}/${instrument}-${spectrumid}-oot.pha \
    #     withspecranges=true energycolumn=PI specchannelmin=0 \
    #     specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
    #     writedss=Y expression="$expr"

    # ESAS type binning
    evselect table=${ootevlist} withimageset=yes imageset=${specdir}/${instrument}-${spectrumid}-oot.im \
        xcolumn=X ycolumn=Y withzcolumn=N withzerrorcolumn=N \
        ximagebinsize=1 yimagebinsize=1 squarepixels=yes \
        ximagesize=900 yimagesize=900 imagebinning=imageSize \
        withxranges=yes ximagemin=3401 ximagemax=48400 withxranges=yes \
        withyranges=yes yimagemin=3401 yimagemax=48400 withyranges=yes \
        withspectrumset=true spectrumset=${specdir}/${instrument}-${spectrumid}-oot.pha \
        withspecranges=true energycolumn=PI specchannelmin=0 \
        specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
        writedss=Y expression="$expr"

fi


# XPROC0  = 'evselect table=pnS003-clean.fits:EVENTS filteredset=filtered.fits w&'
# CONTINUE  'ithfilteredset=yes keepfilteroutput=yes flagcolumn=EVFLAG flagbit=-&'
# CONTINUE  '1 destruct=yes dssblock='''' expression=''(PI in [500:2000]) && (FL&'
# CONTINUE  'AG .eq. 0) && (PATTERN<=4)'' filtertype=expression cleandss=no upda&'
# CONTINUE  'teexposure=yes filterexposure=yes writedss=yes blockstocopy='''' at&'
# CONTINUE  'tributestocopy='''' energycolumn=PHA zcolumn=WEIGHT zerrorcolumn=EW&'
# CONTINUE  'EIGHT withzerrorcolumn=no withzcolumn=no ignorelegallimits=yes imag&'
# CONTINUE  'eset=pnS003-500-2000-woot.im xcolumn=X ycolumn=Y ximagebinsize=1 yi&'
# CONTINUE  'magebinsize=1 squarepixels=yes ximagesize=900 yimagesize=900 imageb&'
# CONTINUE  'inning=imageSize ximagemin=3401 ximagemax=48400 withxranges=yes yim&'
# CONTINUE  'agemin=3401 yimagemax=48400 withyranges=yes imagedatatype=Int32 wit&'
# CONTINUE  'himagedatatype=yes raimagecenter=0 decimagecenter=0 withcelestialce&'
# CONTINUE  'nter=no withimageset=yes spectrumset=spectrum.fits spectralbinsize=&'
# CONTINUE  '10 specchannelmin=0 specchannelmax=4095 withspecranges=no withspect&'
# CONTINUE  'rumset=no rateset=rate.fits timecolumn=TIME timebinsize=1 timemin=0&'
# CONTINUE  ' timemax=1000 withtimeranges=no maketimecolumn=no makeratecolumn=no&'
# CONTINUE  ' withrateset=no histogramset=histo.fits histogramcolumn=TIME histog&'
# CONTINUE  'rambinsize=1 histogrammin=0 histogrammax=1000 withhistoranges=no wi&'
# CONTINUE  'thhistogramset=no # (evselect-3.61) [xmmsas_20110223_1803-11.0.0]'

