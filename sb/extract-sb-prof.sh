######################################################################
# extracts

source ${codedir}/utils/util-funcs-lib.sh

function do_sb_extraction {
    ######################################################################
    # the file input/output names

    outputid=$1

    image=${inst}${prefix}-${elo}-${ehi}.im
    expmap=${inst}${prefix}-${elo}-${ehi}.exp
    bgmap=${inst}${prefix}-${elo}-${ehi}.bg
    mask=${inst}${prefix}-${elo}-${ehi}.mask
    output="sb-prof-${outputid}-"$(date +"%y%m%d")"-${reduction_id}.dat"

    ######################################################################
    # run

    echo ${codedir}/sb/extract-sb-prof.py $image $expmap $bgmap $mask $xim $yim $aperture $output
    ${codedir}/sb/extract-sb-prof.py $image $expmap $bgmap $mask $xim $yim $aperture $output

}

######################################################################
# input parameters

dir=$1
here=`pwd`
cd $dir

elo="500"
ehi="2000"
aperture=50.0                  # [pix]
reduction_id="001"

######################################################################
# get center

pars=(X_IM Y_IM)
out=`get_cluster_pars $pars`
xim=`echo $out | awk '{print $1}'`
yim=`echo $out | awk '{print $2}'`

######################################################################
# extract the profile

# pn
inst=pn
for prefix in $PN_EV_PREFIX_LIST
do
    do_sb_extraction pn
done

# m1
inst=mos1
for prefix in $M1_EV_PREFIX_LIST
do
    do_sb_extraction mos1
done

# m2
inst=mos2
for prefix in $M2_EV_PREFIX_LIST
do
    do_sb_extraction mos2
done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
