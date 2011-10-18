######################################################################
# make simple images with wcs coords in standard bands for quick look

function make-im {

inevli=$1
outim=$2
elo=$3
ehi=$4

evselect \
table=$inevli \
withimageset=yes \
imageset=$outim \
withspectrumset=yes \
spectrumset=$outspec \
withzcolumn=$zcol \
expression="PI>$elo && PI<$ehi && FLAG .eq. 0" \
filteredset=filtered.fits \
withfilteredset=no \
keepfilteroutput=no \
flagcolumn=EVFLAG \
flagbit=-1 \
destruct=yes \
dssblock='' \
filtertype=expression \
cleandss=no \
updateexposure=yes \
filterexposure=yes \
writedss=yes \
blockstocopy='' \
attributestocopy='' \
energycolumn=PHA \
zcolumn=WEIGHT \
zerrorcolumn=EWEIGHT \
withzerrorcolumn=no \
ignorelegallimits=no \
xcolumn=X \
ycolumn=Y \
ximagebinsize=80 \
yimagebinsize=80 \
squarepixels=no \
ximagesize=600 \
yimagesize=600 \
imagebinning=binSize \
ximagemin=1 \
ximagemax=640 \
withxranges=no \
yimagemin=1 \
yimagemax=640 \
withyranges=no \
imagedatatype=Real64 \
withimagedatatype=no \
raimagecenter=0 \
decimagecenter=0 \
withcelestialcenter=no \
spectralbinsize=10 \
specchannelmin=0 \
specchannelmax=4095 \
withspecranges=no \
rateset=rate.fits \
timecolumn=TIME \
timebinsize=1 \
timemin=0 \
timemax=1000 \
withtimeranges=no \
maketimecolumn=no \
makeratecolumn=no \
withrateset=no \
histogramset=histo.fits \
histogramcolumn=TIME \
histogrambinsize=1 \
histogrammin=0 \
histogrammax=1000 \
withhistoranges=no \
withhistogramset=no

}


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