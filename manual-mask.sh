regfile=$1


##########################################################################################################################
# CREATE MASKS FOR PS REMOVAL:
ds9tocxc outset=manual-cheese-template.fits < $regfile

# # Standard:
# thresh1=0.1
# thresh2=0.5

# # Stuntman:
# # thresh1=1e-6
# # thresh2=10.0

# esas defaults
thresh1=0.05
thresh2=5.0

echo -e '\nCreating masks...'

# emask expimageset=pnS003-exp-im.fits   detmaskset=pn-man-mask.fits.cheese   threshold1=$thresh1 threshold2=$thresh2 regionset=manual-cheese-template.fits

# emask expimageset=mos1S001-exp-im.fits detmaskset=m1-man-mask.fits.cheese threshold1=$thresh1 threshold2=$thresh2 regionset=manual-cheese-template.fits

# emask expimageset=mos2S002-exp-im.fits detmaskset=m2-man-mask.fits.cheese threshold1=$thresh1 threshold2=$thresh2 regionset=manual-cheese-template.fits


emask expimageset=comb-exp-im-400-1250.fits detmaskset=pn-man-mask.fits.cheese   threshold1=$thresh1 threshold2=$thresh2 regionset=manual-cheese-template.fits

emask expimageset=comb-exp-im-400-1250.fits detmaskset=m1-man-mask.fits.cheese threshold1=$thresh1 threshold2=$thresh2 regionset=manual-cheese-template.fits

emask expimageset=comb-exp-im-400-1250.fits detmaskset=m2-man-mask.fits.cheese threshold1=$thresh1 threshold2=$thresh2 regionset=manual-cheese-template.fits







# farith pnS003-im1-400-1250.fits 'pnS003-mask-im-det-400-1250.fits[MASK]' pnS003-im1-400-1250-mask.fits MUL copyprime=yes

# pnS003-exp-im-400-1250.fits
# pnS003-exp-im-2000-7200.fits
# pnS003-exp-im.fits
