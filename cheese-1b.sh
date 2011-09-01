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
# prefixm='1S003 2S004'        # mos eventlists
# prefixp="'S005'"             # pn eventlists
# elow=400                     # detection band minimum [eV]
# ehigh=10000                  # detection band maximum [eV]
# scale=0.5                    # source flux extraction fraction
# rate=1.0                     # ps extraction flux threshold [1e14 cgs]
# dist=40.0                    # minimal distance for neighbour ps

prefixm="'1S003 2S004'"      # mos eventlists
prefixp="'S005'"             # pn eventlists
elow=400                     # detection band minimum [eV]
ehigh=10000                  # detection band maximum [eV]
scale=0.5                    # source flux extraction fraction
rate=1.0                     # ps extraction flux threshold [1e14 cgs]
dist=40.0                    # minimal distance for neighbour ps


######################################################################
# cheese using single band detection

cheese prefixm=$prefixm prefixp=$prefixp \
scale=$scale \
rate=$rate \
dist=$dist \
elow=$elow \
ehigh=$ehigh \
clobber=1

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: cheese failed!"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0