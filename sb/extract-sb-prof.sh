######################################################################
# extracts

source ${codedir}/utils/util-funcs-lib.sh

function do_sb_extraction {
    ######################################################################
    # the file input/output names

    outputid=$1                 # [ pn/mos ] note: no mos number!

    image=${inst}${prefix}-${elo}-${ehi}.im
    expmap=${inst}${prefix}-${elo}-${ehi}.exp
    # bgmap=${inst}${prefix}-${elo}-${ehi}.bg
    bgmap=${inst}${prefix}-${elo}-${ehi}.spl.bg
    mask=${inst}${prefix}-${elo}-${ehi}.mask
    output=${sb_dir}/sb-prof-${outputid}-${reduction_id}.dat

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
aperture=100.0                  # [pix]
reduction_id="002"
sb_dir=../sb                    # directory for the sb analysis relative to the analysis dir

######################################################################
# do preparations

mkdir $sb_dir 2> /dev/null

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
inst=mos
for prefix in $M1_EV_PREFIX_LIST
do
    do_sb_extraction mos1
done

# m2
inst=mos
for prefix in $M2_EV_PREFIX_LIST
do
    do_sb_extraction mos2
done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0
