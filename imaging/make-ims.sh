######################################################################
# script extracting images for the imaging pipe

source ${codedir}/utils/util-funcs-lib.sh

dir=$1
here=`pwd`
cd $dir


for prefix in $MOS_EV_PREFIX_LIST
do

elo="500"
ehi="2000"
vignetting=$7

echo make-im mos${prefix}-clean.fits mos${prefix}-im-${elo}-${ehi}.fits $elo $ehi

done




######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0






