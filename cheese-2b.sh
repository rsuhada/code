######################################################################
# runs the esas filters
#
# Snowden & Kuntz, 2011:
#
# cheese and cheese-bands do source detection on the observation
# images and create Swiss cheese masks which can be used later.
# cheese and cheese-bands use the combined source list from emldetect
# for the source excision so the masking for all instruments and
# exposures is the same.  cheese-bands adds the additional ability to
# do the source detection and masking in two bands.

dir=$1
here=`pwd`
cd $dir

######################################################################
# detection settings

# defaults:
# elowlist='400 2000'        # detection bands minima [eV]
# ehighlist='1250 7200'      # detection bands maxima [eV]
# scale=0.5                  # source flux extraction fraction
# ratet=1.0                  # ps extraction total flux threshold [1e14 cgs]
# rates=1.0                  # ps extraction soft flux threshold [1e14 cgs]
# rateh=1.0                  # ps extraction hard flux threshold [1e14 cgs]
# dist=40.0                  # minimal distance for neighbour ps

elowlist='400 2000'        # detection bands minima [eV]
ehighlist='1250 7200'      # detection bands maxima [eV]
scale=0.5                  # source flux extraction fraction
ratet=1.0                  # ps extraction total flux threshold [1e14 cgs]
rates=1.0                  # ps extraction soft flux threshold [1e14 cgs]
rateh=1.0                  # ps extraction hard flux threshold [1e14 cgs]
dist=40.0                  # minimal distance for neighbour ps


######################################################################
# cheese using single band detection

cheese-bands prefixm="$MOS_EV_PREFIX_LIST" prefixp="$PN_EV_PREFIX_LIST" \
elowlist=$elowlist \
ehighlist=$ehighlist \
scale=$scale \
ratet=$ratet \
rates=$rates \
rateh=$rateh \
dist=$dist   \
verb=4       \
clobber=1


if [[ $? -ne 0 ]]
then
    echo -e "\n** error: cheese two band failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0