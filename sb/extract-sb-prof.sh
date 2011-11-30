######################################################################
# extracts

source ${codedir}/utils/util-funcs-lib.sh

dir=$1
here=`pwd`
cd $dir

######################################################################
# input parameters

elo="500"
ehi="2000"
aperture=100.0                  # [pix]

image=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.im
expmap=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.exp
bgmap=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.bg
mask=pn${PN_EV_PREFIX_LIST}-${elo}-${ehi}.mask

######################################################################
# get center

pars=(X_IM Y_IM)
out=`get_cluster_pars $pars`
xim=`echo $out | awk '{print $1}'`
yim=`echo $out | awk '{print $2}'`

######################################################################
# run

echo ${codedir}/sb/extract-sb-prof.py $image $expmap $bgmap $mask $xim $yim $aperture
${codedir}/sb/extract-sb-prof.py $image $expmap $bgmap $mask $xim $yim $aperture

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0