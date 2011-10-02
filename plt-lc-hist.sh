######################################################################
# plot the light curves/diadnostic histograms

dir=$1
here=`pwd`
cd $dir

if [[ ! -e lc ]]
then
    mkdir -p lc/ps
fi


######################################################################
# pn

for i in pn*-hist.qdp
do
prefix=${i:2:4}
echo $prefix

qdp<<EOF
pn${prefix}-hist.qdp
/cps
EOF
mv pgplot.ps lc/ps/pn${prefix}-hist.ps

qdp<<EOF
pn${prefix}-hist.qdp
/gif
EOF
mv pgplot.gif lc/pn${prefix}-hist.gif

done

######################################################################
# mos1

for i in mos1*-hist.qdp
do
prefix=${i:4:4}
echo $prefix

qdp<<EOF
mos1${prefix}-hist.qdp
/cps
EOF
mv pgplot.ps lc/ps/mos1${prefix}-hist.ps

qdp<<EOF
mos1${prefix}-hist.qdp
/gif
EOF
mv pgplot.gif lc/mos1${prefix}-hist.gif

done

######################################################################
# m2

for i in mos2*-hist.qdp
do
prefix=${i:4:4}
echo $prefix

qdp<<EOF
mos2${prefix}-hist.qdp
/cps
EOF
mv pgplot.ps lc/ps/mos2${prefix}-hist.ps

qdp<<EOF
mos2${prefix}-hist.qdp
/gif
EOF
mv pgplot.gif lc/mos2${prefix}-hist.gif

done

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0