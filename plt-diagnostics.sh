######################################################################
# make diagnostic plots

dir=$1
here=`pwd`
cd $dir

format="/gif"
format_suffix="gif"


######################################################################
# prep dir

if [[ ! -e diagnostics ]]
then
    mkdir -p diagnostics/spec
    mkdir -p diagnostics/aug
fi


######################################################################
# diagnostic spectra

for i in *-spec*.qdp
do

echo "plotting :: $i"

qdp<<EOF
$i
$format
EOF

outim=`basename $i .qdp`
mv pgplot.$format_suffix diagnostics/spec/${outim}.$format_suffix

done


######################################################################
# diagnostic hardness ratia

for i in *-aug*.qdp
do

echo "plotting :: $i"

qdp<<EOF
$i
$format
EOF

outim=`basename $i .qdp`
mv pgplot.$format_suffix diagnostics/aug/${outim}.$format_suffix

done


######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0