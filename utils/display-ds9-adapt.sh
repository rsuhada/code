######################################################################
# small local utility script for nice ds9 display
#
# TODO: add adaptive cuts based on redshift and flux
# TODO: add region file check/handling
# TODO: write the path from $DS9_BINARY

image=adapt-500-2000.fits

/Applications/SAOImage\ DS9.app/Contents/MacOS/ds9 $image \
-regions load cluster-man-01.wcs.reg \
-regions load ps-man-01.wcs.reg \
-regions load bg-ann-01.wcs.reg \
-cmap SLS \
-cmap value 0.97 0.541 \
-scale linear \
-zoom 0.65 \
