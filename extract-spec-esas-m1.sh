######################################################################
# runs the esas filters
#
# Snowden & Kuntz, 2011:
#
# mos-spectra and pn-spectra processes the filtered event files to
# produce background spectra for the entire energy range and selected
# region and background images for the selected region and selected
# band for the individual ccds.  The region selection expression is in
# an input file and should be in detector coordinates.  If the input
# file does not exist, reg.txt in this case, the default is to process
# the entire FOV.  The input energies are in eV.  Change the caldb
# directory string to whatever is appropriate.  In this step the
# processing is to create images in two bands for the instruments.


dir=$1
here=`pwd`
cd $dir

######################################################################
# spectrum extraction setup

# defaults:
prefix="'1S003'"      # mos eventlists
elow='400'        # detection bands minima [eV]
ehigh='1250'      # detection bands maxima [eV]
regfile=reg.txt

######################################################################
# extract m1 spectra

mos-spectra prefix=$prefix caldb=$esas_caldb region=$regfile mask=1 elow=$elow ehigh=$ehigh ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7

# CONTINUE HERE

mos-spectra prefix=1S003 caldb=/XMM/sas/CCF/esas region=reg.txt mask=1 elow=2000 ehigh=7200 ccd1=1 ccd2=1 ccd3=1 ccd4=1 ccd5=0 ccd6=1 ccd7=1


if [[ $? -ne 0 ]]
then
    echo -e "\n** error: spectral extraction failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0