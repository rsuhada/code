######################################################################
# make simple images with wcs coords in standard bands for quick look

source ${codedir}/utils/util-funcs-lib.sh

######################################################################
# main

dir=$1
here=`pwd`
cd $dir

M1_EV_PREFIX=$M1_EV_PREFIX_LIST
M2_EV_PREFIX=$M2_EV_PREFIX_LIST
PN_EV_PREFIX=$PN_EV_PREFIX_LIST


elo=300
ehi=500

make-im mos${M1_EV_PREFIX}-clean.fits mos${M1_EV_PREFIX}-quick-im-${elo}-${ehi}.fits $elo $ehi
make-im mos${M2_EV_PREFIX}-clean.fits mos${M2_EV_PREFIX}-quick-im-${elo}-${ehi}.fits $elo $ehi
make-im pn${PN_EV_PREFIX}-clean.fits  pn${PN_EV_PREFIX}-quick-im-${elo}-${ehi}.fits  $elo $ehi


elo=500
ehi=2000

make-im mos${M1_EV_PREFIX}-clean.fits mos${M1_EV_PREFIX}-quick-im-${elo}-${ehi}.fits $elo $ehi
make-im mos${M2_EV_PREFIX}-clean.fits mos${M2_EV_PREFIX}-quick-im-${elo}-${ehi}.fits $elo $ehi
make-im pn${PN_EV_PREFIX}-clean.fits  pn${PN_EV_PREFIX}-quick-im-${elo}-${ehi}.fits  $elo $ehi


elo=2000
ehi=7000

make-im mos${M1_EV_PREFIX}-clean.fits mos${M1_EV_PREFIX}-quick-im-${elo}-${ehi}.fits $elo $ehi
make-im mos${M2_EV_PREFIX}-clean.fits mos${M2_EV_PREFIX}-quick-im-${elo}-${ehi}.fits $elo $ehi
make-im pn${PN_EV_PREFIX}-clean.fits  pn${PN_EV_PREFIX}-quick-im-${elo}-${ehi}.fits  $elo $ehi


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0