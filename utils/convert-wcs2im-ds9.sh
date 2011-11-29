######################################################################
# converts a wcs ds9 region to image coordinates
#
# NOTE: requires X-session, opens ds9 window
# FIXME: implement an ad2xy.pro like solution that doesn't need ds9

im=$1
region_file=$2
outreg=${region_file}

outreg=`basename ${region_file} .phy.reg`.im.reg

/Applications/SAOImage\ DS9.app/Contents/MacOS/ds9 $im \
	-regions format ds9 \
	-regions load $region_file \
	-regions system image \
    -region save $outreg \
    -exit