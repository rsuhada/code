######################################################################
# runs the esas filters
#
# Snowden & Kuntz, 2011:
#
# mos-filter and pn-filter run the SAS task espfilt (along with a few
# others). espfilt filters and cleans the event files of obvious soft
# proton events, and then produces QDP plot files showing the light
# curves and the accepted time intervals.  Note that while much of the
# SP contamination is removed there is likely to be some residual
# contamination left.


dir=$1
here=`pwd`
cd $dir


######################################################################
# pn

echo -e "\nRunning pn filter"
pn-filter

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: pn-filter failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# mos

echo -e "\nRunning mos filter"
mos-filter


if [[ $? -ne 0 ]]
then
    echo -e "\n** error: mos-filter failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# clean up temporary files

rm -f *.FIT


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0