######################################################################
# backscale factor for spectroscopy

######################################################################
# inputs

instrument=$1
spectrumid=$2
specdir=$3

######################################################################
# select the proper eventlis

case $instrument in
    "pn")
        prefix=$PN_EV_PREFIX_LIST
        evlist=pn${prefix}-clean.fits
        ;;
    "m1")
        prefix=$M1_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        ;;
    "m2")
        prefix=$M2_EV_PREFIX_LIST
        evlist=mos${prefix}-clean.fits
        ;;
    *)
        echo "unknown instrument!"
        exit 1
esac

######################################################################
# do the backscal calculation

backscale spectrumset=${specdir}/${instrument}-${spectrumid}.pha badpixlocation=$evlist useodfatt=yes