######################################################################
# extracts a sb profiles (also cumulative profiles)

source ${codedir}/utils/util-funcs-lib.sh

function do_sb_extraction {
    ######################################################################
    # the file input/output names

    outputid=$1                 # [ pn/mos ] note: no mos number!

    image=${inst}${prefix}-${elo}-${ehi}.im
    expmap=${inst}${prefix}-${elo}-${ehi}.exp
    bgmap=${inst}${prefix}-${elo}-${ehi}${bg_type_id}.bg
    mask=${inst}${prefix}-${elo}-${ehi}.mask
    output=${sb_dir}/sb-prof-${outputid}-${reduction_id}.dat

    ######################################################################
    # run

    echo $PYTHONEXEC ${codedir}/sb/extract-sb-prof.py $image $expmap $bgmap $mask $xim $yim $rmin $rmax $binning $output
    $PYTHONEXEC ${codedir}/sb/extract-sb-prof.py $image $expmap $bgmap $mask $xim $yim $rmin $rmax $binning $output

    if [[ $PLOT_CUMUL_PROF -eq 1 ]]
    then
        $PYTHONEXEC ${codedir}/sb/plt_cumul_sb.py ${output}.cumul
    fi
}

######################################################################
# input parameters

dir=$1
here=`pwd`
cd $dir

reduction_id="001"              # FIXME: add autonaming - see below
elo="500"
ehi="2000"
rmin=0.0                    # [pix]
rmax=200.0                  # [pix]
binning=1.0                 # either fixed-width bin, or "a11", "m13"
# bg_type_id=".spl"               # "" - 2comp, ".spl" - spline
bg_type_id=""               # "" - 2comp, ".spl" - spline
sb_dir=../sb                    # directory for the sb analysis relative to the analysis dir
PLOT_CUMUL_PROF=1               # make a quick view plot?

######################################################################
# assign profile ID - keep in sync with the naming convention in
# do_sb_extraction

# # FIXME: add incrementing
# reduction_id=`ls -rt1 ${sb_dir}/sb-prof*.dat | tail -1 | sed 's/.*\///g'| cut -c 14-16`

# echo $reduction_id
# sleep 5

# if [[ "$reduction_id" == "" ]]
# then
#     reduction_id=001
# fi

check_file=`ls -rt1 ${sb_dir}/sb-prof*-${reduction_id}.dat  | tail -1`

if [[ -e ${check_file} ]]
then
    echo -e "\n** error: ${check_file} already exists here!"
    echo -e "*** error in $0\n"
    cd $startdir
    exit 1
fi

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
