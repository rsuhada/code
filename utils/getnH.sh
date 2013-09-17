if [ $# -lt 2 ]
then
	echo "Returns the Weighted nH value for given coord."
	echo
	echo "Example: "
	echo "getnH.sh 355.691 -54.1831"
	echo
	echo "Output: both D&L and LAB vals and their rel. difference in % wrt D&L."
else

    ra=$1
    de=$2

    echo
    echo "#############################################################################"
    nh equinox=2000 ra=$ra dec=$de usemap=1 | tee nh.tmp
    # nh equinox=2000 ra=$ra dec=$de usemap=1 > nh.tmp
    echo "#############################################################################"
    nh equinox=2000 ra=$ra dec=$de usemap=0 | tee -a nh.tmp
    # nh equinox=2000 ra=$ra dec=$de usemap=1 > nh.tmp

     dl=`cat nh.tmp | grep "DL >> Weighted average nH" | awk '{print $7}'`
    lab=`cat nh.tmp | grep "LAB >> Weighted average nH" | awk '{print $7}'`
    rel_diff=`~/data1/sw/calc/calc.pl 100\*\($dl - $lab\)/$dl`


    echo "#############################################################################"
    echo
    echo
    echo "# ra de dl lab rel_diff_wrt_dl"
    echo $ra $de $dl $lab $rel_diff

    rm nh.tmp
fi

echo
echo "results written to :: getnH.sh.results"