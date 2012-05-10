######################################################################
# runs spectral extraction in the requested bands
#
# Snowden & Kuntz, 2011:
#
# pn-spectra and pn-spectra processes the filtered event files to
# produce background spectra for the entire energy range and selected
# region and background images for the selected region and selected
# band for the individual ccds.  The region selection expression is in
# an input file and should be in detector coordinates.  If the input
# file does not exist, reg.txt in this case, the default is to process
# the entire FOV.  The input energies are in eV.  Change the caldb
# directory string to whatever is appropriate.  In this step the
# processing is to create images in two bands for the instruments.

dir=$1
elow=$2            # detection bands minima [eV]
ehigh=$3          # detection bands maxima [eV]
here=`pwd`
cd $dir

######################################################################
# extract pn spectra - standard band

prefix=$PN_EV_PREFIX_LIST
regfile=$PN_SRC_REGFILE
pattern=4
quad1=$PN_QUAD1
quad2=$PN_QUAD2
quad3=$PN_QUAD3
quad4=$PN_QUAD4

pn-spectra prefix="$prefix" caldb=$esas_caldb region=$regfile mask=1 elow="$elow" ehigh="$ehigh" pattern=4 quad1=$quad1 quad2=$quad2 quad3=$quad3 quad4=$quad4

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: pn spectral extraction in standard band failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0