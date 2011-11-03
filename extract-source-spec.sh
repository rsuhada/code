######################################################################
# inputs

instrument=$1
SRC_REGION=$2
PS_REGION=$3


######################################################################
# parse the region files, second parameter equals 0 means region file
# will be removed

ds9reg_to_sasdesc $SRC_REGION 1
ds9reg_to_sasdesc $PS_REGION 0


######################################################################
# prepare the region descriptors

inpattern=`cat ${PS_REGION}.desc`
psreg="$inpattern"

inpattern=`cat ${SRC_REGION}.desc`
srcreg="$inpattern"


if [[ "$instrument" == "pn" ]]
then
    instpattern="((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=4) && (PI in [100:10000])"
    prefix=$M1_EV_PREFIX_LIST
else
    instpattern="#XMMEA_EM && ((FLAG & 0x10000) == 0) && (FLAG == 0) && (PATTERN<=12) && (PI in [100:10000])"
fi


case $instrument in
    "pn")

        ;;
    "m1")

        ;;
    "m2")

        ;;
    *)
        echo "unknown instrument!"
        exit 1
esac




######################################################################
#  get source spectra

echo -e '\nGetting m1 spectra...'

expr="$instpattern && $srcreg $psreg"
evlist=mos${prefix}-clean.fits

evselect table=${evlist} withimageset=yes imageset=${specdir}/m1.im \
    xcolumn=X ycolumn=Y imagebinning=binSize ximagebinsize=80 \
    yimagebinsize=80 withzcolumn=N withzerrorcolumn=N \
    withspectrumset=true spectrumset=${specdir}/m1.pha \
    withspecranges=true energycolumn=PI specchannelmin=0 \
    specchannelmax=11999 spectralbinsize=5 updateexposure=yes \
    writedss=Y expression="$mosexpr"


