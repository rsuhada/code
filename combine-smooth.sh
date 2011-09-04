######################################################################
# rename extracted products with their analysis_id


dir=$1
here=`pwd`
cd $dir

analysis_id=$ANALYSIS_ID

# FIXME: what is passed is potentially a list - should loop through files
M1_EV_PREFIX=$M1_EV_PREFIX_LIST
M2_EV_PREFIX=$M2_EV_PREFIX_LIST
PN_EV_PREFIX=$PN_EV_PREFIX_LIST


######################################################################
# soft band

elow='400'            # detection bands minima [eV]
ehigh='1250'          # detection bands maxima [eV]


######################################################################
# use comb once more to combine exposures, this time with point
# sources masked using the cheese images.

comb caldb=${esas_caldb} withpartcontrol=1 withsoftcontrol=1 withswcxcontrol=0 nbands=1 elowlist=$elow ehighlist=$ehigh mask=1 ndata=3 prefixlist="${M1_EV_PREFIX} ${M2_EV_PREFIX} ${PN_EV_PREFIX}"


######################################################################
# adapt-900 adaptively smooths the images.

adapt_900 smoothingcounts=50 thresholdmasking=0.02 detector=0 binning=2 elow=$ehigh ehigh=$elow withmaskcontrol=no withpartcontrol=yes withsoftcontrol=yes withswcxcontrol=0


######################################################################
# hard band

elow='2000'            # detection bands minima [eV]
ehigh='7200'          # detection bands maxima [eV]


######################################################################
# use comb once more to combine exposures, this time with point
# sources masked using the cheese images.

comb caldb=${esas_caldb} withpartcontrol=1 withsoftcontrol=1 withswcxcontrol=0 nbands=1 elowlist=$elow ehighlist=$ehigh mask=1 ndata=3 prefixlist="${M1_EV_PREFIX} ${M2_EV_PREFIX} ${PN_EV_PREFIX}"


######################################################################
# adapt-900 adaptively smooths the images.

adapt_900 smoothingcounts=50 thresholdmasking=0.02 detector=0 binning=2 elow=$ehigh ehigh=$elow withmaskcontrol=no withpartcontrol=yes withsoftcontrol=yes withswcxcontrol=0


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0

