######################################################################
# rename extracted products with their analysis_id


dir=$1
here=`pwd`
cd $dir

analysis_id=$ANALYSIS_ID

# FIXME: what is passed is potentially a list - should loop through files
M1_EV_PREFIX=$M1_EV_PREFIX_LIST
M2_EV_PREFIX=$M2_EV_PREFIX_LIST
PN_EV_PREFIX=$PN_EV_PREFIX_LIST

######################################################################
# comb combines exposures 0 ps are masked

elow='400'            # detection bands minima [eV]
ehigh='1250'          # detection bands maxima [eV]

comb caldb=${esas_caldb} withpartcontrol=1 withsoftcontrol=0 withswcxcontrol=0 nbands=1 elowlist=$elow ehighlist=$ehigh mask=1 ndata=3 prefixlist="${M1_EV_PREFIX} ${M2_EV_PREFIX} ${PN_EV_PREFIX}"

elow='500'            # detection bands minima [eV]
ehigh='2000'          # detection bands maxima [eV]

comb caldb=${esas_caldb} withpartcontrol=1 withsoftcontrol=0 withswcxcontrol=0 nbands=1 elowlist=$elow ehighlist=$ehigh mask=1 ndata=3 prefixlist="${M1_EV_PREFIX} ${M2_EV_PREFIX} ${PN_EV_PREFIX}"

elow='2000'            # detection bands minima [eV]
ehigh='7200'          # detection bands maxima [eV]

comb caldb=${esas_caldb} withpartcontrol=1 withsoftcontrol=0 withswcxcontrol=0 nbands=1 elowlist=$elow ehighlist=$ehigh mask=1 ndata=3 prefixlist="${M1_EV_PREFIX} ${M2_EV_PREFIX} ${PN_EV_PREFIX}"


# ######################################################################
# # manual ps removal solution sketch

# # esas defaults
# thresh1=0.05
# thresh2=5.0

# emask expimageset=comb-exp-im-400-1250.fits detmaskset=man-mask.fits.cheese   threshold1=$thresh1 threshold2=$thresh2 regionset=manual-cheese-template.fits

# image=comb-back-im-sky-400-1250.fits
# farith $image 'man-mask.fits.cheese[MASK]' farith.tmp.fits MUL copyprime=yes clobber=yes
# mv farith.tmp.fits $image

# image=comb-exp-im-400-1250.fits
# farith $image 'man-mask.fits.cheese[MASK]' farith.tmp.fits MUL copyprime=yes clobber=yes
# mv farith.tmp.fits $image

# image=comb-obj-im-400-1250.fits
# farith $image 'man-mask.fits.cheese[MASK]' farith.tmp.fits MUL copyprime=yes clobber=yes
# mv farith.tmp.fits $image

# image=comb-prot-im-sky-400-1250.fits
# farith $image 'man-mask.fits.cheese[MASK]' farith.tmp.fits MUL copyprime=yes clobber=yes
# mv farith.tmp.fits $image


######################################################################
# adapt-900 adaptively smooths the images.

# adapt_900 smoothingcounts=50 thresholdmasking=0.02 detector=0 binning=2 elow=$ehigh ehigh=$elow withmaskcontrol=no withpartcontrol=yes withsoftcontrol=yes withswcxcontrol=0

# adapt_900 smoothingcounts=10 thresholdmasking=0.02 detector=0 binning=1 elow=$elow ehigh=$ehigh withmaskcontrol=no withpartcontrol=no withsoftcontrol=no withswcxcontrol=0

# adapt_900 smoothingcounts=50 thresholdmasking=0.02 detector=0 binning=1 elow=$elow ehigh=$ehigh withmaskcontrol=no withpartcontrol=1 withsoftcontrol=0 withswcxcontrol=0

elow=400
ehigh=1250
adapt_900 smoothingcounts=50 thresholdmasking=0.02 detector=0 binning=1 elow=$elow ehigh=$ehigh withmaskcontrol=no withpartcontrol=1 withsoftcontrol=0 withswcxcontrol=0

elow=500
ehigh=2000
adapt_900 smoothingcounts=50 thresholdmasking=0.02 detector=0 binning=1 elow=$elow ehigh=$ehigh withmaskcontrol=no withpartcontrol=1 withsoftcontrol=0 withswcxcontrol=0

elow=2000
ehigh=7200
adapt_900 smoothingcounts=50 thresholdmasking=0.02 detector=0 binning=1 elow=$elow ehigh=$ehigh withmaskcontrol=no withpartcontrol=1 withsoftcontrol=0 withswcxcontrol=0

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0

