######################################################################
# do the calculations required for soft-proton contamination
# correction

dir=$1
here=`pwd`
cd $dir

analysis_id=$ANALYSIS_ID


# FIXME: what is passed is potentially a list - should loop through files
M1_EV_PREFIX=$M1_EV_PREFIX_LIST
M2_EV_PREFIX=$M2_EV_PREFIX_LIST
PN_EV_PREFIX=$PN_EV_PREFIX_LIST

######################################################################
# evigweight the eventlists

inevli=mos${M1_EV_PREFIX}-clean.fits
evigweight ineventset=$inevli witheffectivearea=yes withquantumefficiency=yes withfiltertransmission=yes
inevli=mos${M2_EV_PREFIX}-clean.fits
evigweight ineventset=$inevli witheffectivearea=yes withquantumefficiency=yes withfiltertransmission=yes
inevli=pn${PN_EV_PREFIX}-clean.fits
evigweight ineventset=$inevli witheffectivearea=yes withquantumefficiency=yes withfiltertransmission=yes




######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0


