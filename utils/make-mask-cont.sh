######################################################################
# creates a auxiliary ds9 region file from a mask (useful for masking
# efficiency check)
#
# NOTE: requires X-session, opens ds9 window, needs standard region
# naming (e.g. *.wcs.reg)

if [[ $# -lt 1 ]]
then
    echo
    echo "** error in $0"
    echo "*** One parameter required: missing!"
    echo "*** Call example:"
    echo "*** $0 pnS003-cheese.fits"
    exit 0
fi

im=$1

# if you want a .con file:
# -contour save ${im}.wcs.con wcs fk5 \

/Applications/SAOImage\ DS9.app/Contents/MacOS/ds9 $im \
    -contour levels "0 1" \
    -contour nlevels 1 \
    -contour smooth 1 \
    -contour generate \
    -contour color orange \
    -contour width 1 \
    -contour yes \
    -contour convert \
    -regions system wcs \
    -regions save ${im}.wcs.reg \
    -regions system wcs \
    -exit
