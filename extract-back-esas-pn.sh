######################################################################
# runs spectral extraction in the esas bands
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
# like: mos1S003-spec.qdp
# rot-im-det-sky uses information in a previously created count image
# in sky coordinates to rotate the detector coordinate background
# images into images in sky coordinates.


dir=$1
here=`pwd`
cd $dir


######################################################################
# extract pn spectra - soft band

prefix=$PN_EV_PREFIX_LIST
elow='400'      # detection bands minima [eV]
ehigh='1250'    # detection bands maxima [eV]
quad1=$PN_QUAD1
quad2=$PN_QUAD2
quad3=$PN_QUAD3
quad4=$PN_QUAD4


pn_back prefix="$prefix" caldb=$esas_caldb diag=0 elow=$elow ehigh=$ehigh quad1=$quad1 quad2=$quad2 quad3=$quad3 quad4=$quad4

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: pn background extraction in soft band failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# rotate background to sky position

rot-im-det-sky prefix="$prefix" mask=0 elow=$elow ehigh=$ehigh mode=1

######################################################################
# extract pn spectra - soft band

prefix=$PN_EV_PREFIX_LIST
elow='2000'     # detection bands minima [eV]
ehigh='7200'    # detection bands maxima [eV]
quad1=$PN_QUAD1
quad2=$PN_QUAD2
quad3=$PN_QUAD3
quad4=$PN_QUAD4


pn_back prefix="$prefix" caldb=$esas_caldb diag=0 elow=$elow ehigh=$ehigh quad1=$quad1 quad2=$quad2 quad3=$quad3 quad4=$quad4

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: pn background extraction in hard band failed!"
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