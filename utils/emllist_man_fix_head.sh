######################################################################
# simple script to fix emllfirs-man.fits headers so that they are SAS
# compliant just as standard emllist.fits
# run after manual ps removal in the analysis/ dir

cp emllist.fits tmp_emllist.fits
fdelhdu tmp_emllist.fits+1 N Y
fappend emllist-man.fits+1 tmp_emllist.fits
mv tmp_emllist.fits emllist-man.fits

echo "header fixed!"