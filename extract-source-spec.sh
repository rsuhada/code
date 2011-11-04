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

######################################################################
# parse the region files, second parameter equals 0 means region file
# will be removed, prepare the region descriptors

ds9reg_to_sasdesc $SRC_REGION 1
inpattern=`cat ${SRC_REGION}.desc`
srcreg="$inpattern"

if [[ $# -ne 5 ]]
then
    echo -e "No point source region file provided"
    psreg=""
else
    ds9reg_to_sasdesc $PS_REGION 0
    inpattern=`cat ${PS_REGION}.desc`
    psreg="$inpattern"
fi

######################################################################
# select the eventlist and the selection pattern

case $instrument in
    "pn")
        instpattern="((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=4) && (PI in [100:10000])"
        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
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

echo -e '\nGetting m1 spectra...'

expr="$instpattern && $srcreg $psreg"

evselect table=${evlist} withimageset=yes imageset=${specdir}/${instrument}-${spectrumid}.im \
    xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
    yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
    withspectrumset=true spectrumset=${specdir}/${instrument}-${spectrumid}.pha \
    withspecranges=true energycolumn=PI specchannelmin=0 \
    specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
    writedss=Y expression="$expr"