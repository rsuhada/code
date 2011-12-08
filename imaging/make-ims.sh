######################################################################
# script extracting images for the imaging pipe

source ${codedir}/utils/util-funcs-lib.sh

dir=$1
here=`pwd`
cd $dir

######################################################################
# extraction for the 0.5-2 keV band

elo="500"
ehi="2000"

pattern="&& (PATTERN<=12)"
m1ccdpattern=$(eval_ccd_pattern m1)
m2ccdpattern=$(eval_ccd_pattern m2)

# m1
for prefix in $M1_EV_PREFIX_LIST
do
    echo make-im mos${prefix}-clean.fits mos${prefix}-${elo}-${ehi}.im $elo $ehi "$pattern && $m1ccdpattern"
    make-im mos${prefix}-clean.fits mos${prefix}-${elo}-${ehi}.im $elo $ehi "$pattern && $m1ccdpattern"
done

# m2
for prefix in $M2_EV_PREFIX_LIST
do
    echo make-im mos${prefix}-clean.fits mos${prefix}-${elo}-${ehi}.im $elo $ehi "$pattern && $m2ccdpattern"
    make-im mos${prefix}-clean.fits mos${prefix}-${elo}-${ehi}.im $elo $ehi "$pattern && $m2ccdpattern"
done

# pn
pattern="&& (PATTERN<=4)"

for prefix in $PN_EV_PREFIX_LIST
do
    echo make-im pn${prefix}-clean.fits pn${prefix}-${elo}-${ehi}.im $elo $ehi "$pattern"
    make-im pn${prefix}-clean.fits pn${prefix}-${elo}-${ehi}-woot.im $elo $ehi "$pattern"

    # oot subtraction
    make-im pn${prefix}-clean-oot.fits pn${prefix}-${elo}-${ehi}-oot.im $elo $ehi "$pattern"

    # FIXME: implement!
    subtract-oot pn${prefix}-${elo}-${ehi}-woot.im pn${prefix}-${elo}-${ehi}-oot.im pn${prefix}-${elo}-${ehi}.im
done



######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0




