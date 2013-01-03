######################################################################
# start the SB analysis

source ${codedir}/utils/util-funcs-lib.sh

dir=$1
here=`pwd`
cd $dir

######################################################################
# input parameters

elo="500"
ehi="2000"
aperture=80.0

pars=(X_IM Y_IM)
out=`get_cluster_pars $pars`
xim=`echo $out | awk '{print $1}'`
yim=`echo $out | awk '{print $2}'`

outfile="cts-aper-stat.log"

######################################################################
# run

image=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.im
bgmap=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.bg
expmap=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.exp

$PYTHONEXEC ${codedir}/sb/get_cts_stat_aper.py $image $xim $yim $aperture $bgmap | tee >> $outfile

image=mos${M1_EV_PREFIX_LIST}-${elo}-${ehi}.im
bgmap=mos${M1_EV_PREFIX_LIST}-${elo}-${ehi}.bg
expmap=mos${M1_EV_PREFIX_LIST}-${elo}-${ehi}.exp

$PYTHONEXEC ${codedir}/sb/get_cts_stat_aper.py $image $xim $yim $aperture $bgmap | tee >> $outfile

# mos2
image=mos${M2_EV_PREFIX_LIST}-${elo}-${ehi}.im
bgmap=mos${M2_EV_PREFIX_LIST}-${elo}-${ehi}.bg
expmap=mos${M2_EV_PREFIX_LIST}-${elo}-${ehi}.exp

$PYTHONEXEC ${codedir}/sb/get_cts_stat_aper.py $image $xim $yim $aperture $bgmap | tee >> $outfile

######################################################################
#  output report

echo
echo "###################################"
echo "image  :: " $image
echo "bgmap  :: " $bgmap
echo "expmap :: " $expmap
echo "###################################"
echo "xim    :: " $xim
echo "yim    :: " $yim
echo "###################################"
echo

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0