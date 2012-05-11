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
# get prefix list and save the raw eventlists

pnprefix_string="export PN_EV_PREFIX_LIST='"
m1prefix_string="export M1_EV_PREFIX_LIST='"
m2prefix_string="export M2_EV_PREFIX_LIST='"
m3prefix_string="export MOS_EV_PREFIX_LIST='"

for evli in mos1????-ori.fits
do
    prefix=`echo ${evli:3:5}`
    echo $evli
    echo $prefix
    ln -s mos${prefix}-obj-im.fits m1-aux.im
    m1prefix_string="${m1prefix_string}${prefix} "
    m3prefix_string="${m3prefix_string}${prefix} "
    echo $m3prefix_string

done

for evli in mos2????-ori.fits
do
    prefix=`echo ${evli:3:5}`
    echo $evli
    echo $prefix
    ln -s mos${prefix}-obj-im.fits m2-aux.im
    m2prefix_string="${m2prefix_string}${prefix} "
    m3prefix_string="${m3prefix_string}${prefix} "
done


for evli in pn????-ori.fits
do
    prefix=`echo ${evli:2:4}`
    echo $evli
    echo $prefix
    ln -s pn${prefix}-obj-im.fits pn-aux.im
    pnprefix_string="${pnprefix_string}${prefix} "
done

pnprefix_string=${pnprefix_string%?}"'"
m1prefix_string=${m1prefix_string%?}"'"
m2prefix_string=${m2prefix_string%?}"'"
m3prefix_string=${m3prefix_string%?}"'"

echo
echo "Prefixes:"
(
echo
echo $pnprefix_string
echo $m1prefix_string
echo $m2prefix_string
echo $m3prefix_string
echo
) | tee -a $NOTESFILE

# clean up temporary files
rm -f *.FIT

# produce diagnostic quickview plots
${codedir}/plt-lc-hist.sh .

# write a reminder
echo "REMINDER: inspect light curves"
echo "REMINDER: select proper eventlist prefixes"

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0