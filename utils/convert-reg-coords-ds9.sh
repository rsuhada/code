######################################################################
# converts an ds9 region to image/wcs/wcs60/phys coordinates
#
# NOTE: requires X-session, opens ds9 window, needs standard region
# naming (e.g. *.wcs.reg)
# FIXME: implement an ad2xy.pro like solution that doesn't need ds9
# (parts exist through ecoordconvert)

if [[ $# -lt 2 ]]
then
    echo
    echo "** error in $0"
    echo "*** Two parameters required: missing one or more!"
    echo "*** Call example:"
    echo "*** convert-reg-coords-ds9.sh comb-obj-im-2000-7200.fits cluster-man-01.wcs.reg"
    exit 0
fi

im=$1
region_file=$2
outreg=${region_file%.*.*}

mv $region_file conversion_tmp.reg

$DS9_BINARY $im \
	-regions format ds9 \
	-regions load conversion_tmp.reg \
	-regions system image \
    -regions save ${outreg}.im.reg \
    -regions system physical \
    -regions save ${outreg}.phy.reg \
    -regions system wcs \
    -regions save ${outreg}.wcs.reg \
    -regions system wcs \
    -regions skyformat sexagesimal \
    -regions save ${outreg}.wcs60.reg \
    -exit

# rather to keep in case you accidentaly overwritten the good region
# files (if image had regions in header...)
cp conversion_tmp.reg $region_file