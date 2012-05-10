######################################################################
# runs spectral extraction in the esas bands
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
# extract m1 spectra - soft band

prefix=$M1_EV_PREFIX_LIST      # mos eventlists
elow='400'            # detection bands minima [eV]
ehigh='1250'          # detection bands maxima [eV]
regfile=$M1_SRC_REGFILE
ccd1=$M1_CCD1
ccd2=$M1_CCD2
ccd3=$M1_CCD3
ccd4=$M1_CCD4
ccd5=$M1_CCD5
ccd6=$M1_CCD6
ccd7=$M1_CCD7


mos-spectra prefix="$prefix" caldb=$esas_caldb region=$regfile mask=1 elow=$elow ehigh=$ehigh ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: mos1 spectral extraction in soft band failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# extract m1 spectra - hard band

prefix=$M1_EV_PREFIX_LIST      # mos eventlists
elow='2000'            # detection bands minima [eV]
ehigh='7200'          # detection bands maxima [eV]
regfile=$M1_SRC_REGFILE
ccd1=$M1_CCD1
ccd2=$M1_CCD2
ccd3=$M1_CCD3
ccd4=$M1_CCD4
ccd5=$M1_CCD5
ccd6=$M1_CCD6
ccd7=$M1_CCD7


mos-spectra prefix=$prefix caldb=$esas_caldb region=$regfile mask=1 elow=$elow ehigh=$ehigh ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7


if [[ $? -ne 0 ]]
then
    echo -e "\n** error: mos1 spectral extraction in hard band failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi

# # part refactored to its own script in extract-spec-band
# ######################################################################
# # extract m1 spectra - standard band

# prefix=$M1_EV_PREFIX_LIST      # mos eventlists
# elow='500'            # detection bands minima [eV]
# ehigh='2000'          # detection bands maxima [eV]
# regfile=$M1_SRC_REGFILE
# ccd1=$M1_CCD1
# ccd2=$M1_CCD2
# ccd3=$M1_CCD3
# ccd4=$M1_CCD4
# ccd5=$M1_CCD5
# ccd6=$M1_CCD6
# ccd7=$M1_CCD7


# mos-spectra prefix=$prefix caldb=$esas_caldb region=$regfile mask=1 elow=$elow ehigh=$ehigh ccd1=$ccd1 ccd2=$ccd2 ccd3=$ccd3 ccd4=$ccd4 ccd5=$ccd5 ccd6=$ccd6 ccd7=$ccd7


# if [[ $? -ne 0 ]]
# then
#     echo -e "\n** error: mos1 spectral extraction in standard band failed!"
#     echo -e "*** error in script: $0\n"
#     cd $startdir
#     exit 1
# fi

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0