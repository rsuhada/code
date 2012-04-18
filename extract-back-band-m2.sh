######################################################################
# runs background spectral extraction in the custom bands
#
# Snowden & Kuntz, 2011:
#
# mos-back and pn-back take the individual ccd or quadrant spectra and
# images and combines them into complete spectra and images for the
# selected region.  The resultant image is in detector coordinates.
# mos-back creates a QDP plot file which shows the source and model
# background spectra for the observation.  Any discrepancies at higher
# energies probably indicate residual soft proton contamination,
# unless there are really hard and bright sources in the field.  In
# the case of this observation the discrepancy at high energies is
# consistent with soft protons as a residual contamination was already
# expected from the light curve histogram.  The QDP files have names
# like: mos2S003-spec.qdp
# rot-im-det-sky uses information in a previously created count image
# in sky coordinates to rotate the detector coordinate background
# images into images in sky coordinates.


dir=$1
elow=$2            # detection bands minima [eV]
ehigh=$3          # detection bands maxima [eV]
here=`pwd`
cd $dir


######################################################################
# extract m2 spectra - soft band

prefix=$M2_EV_PREFIX_LIST
ccd1=$M2_CCD1
ccd2=$M2_CCD2
ccd3=$M2_CCD3
ccd4=$M2_CCD4
ccd5=$M2_CCD5
ccd6=$M2_CCD6
ccd7=$M2_CCD7


mos_back prefix="$prefix" caldb=$esas_caldb diag=0 elow="$elow" ehigh="$ehigh" ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: mos2 background extraction in soft band failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi

######################################################################
# rotate background to sky position

rot-im-det-sky prefix="$prefix" mask=0 elow=$elow ehigh=$ehigh mode=1

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0