######################################################################
# prepares an odf dir for esas analysis
# i.e.: renames dir to odf, unpacks files
# it is supposed to be run from within $obsid directory

dir=$1
here=`pwd`
cd $dir

echo -e "\npreparing odf directory :: " $1

if [[ -e ODF ]]
then
    mv ODF odf
fi

if [[ -e odf ]]
then
    cd odf
    gunzip *.gz
else
    cd $startdir
    echo -e "\n** error: obsid $obsid does not contain ODF directory"
    echo -e "error in script: $0\n"
    exit 1
fi

cd ../

if [[ ! -e analysis ]]
then
    mkdir analysis
fi

cd $here
echo -e "\nodf directory prepared"
exit 0