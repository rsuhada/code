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
    tar -xvvf *.tar
    tar -xvvf *.TAR
else
    cd $startdir
    echo -e "\n** error: obsid $obsid does not contain ODF directory"
    echo -e "*** error in script: $0\n"
    exit 1
fi

cd ../

if [[ ! -e analysis ]]
then
    mkdir analysis
    echo "${dir}/analysis ${dir}/odf" > analysis/obsid-list.txt
fi

if [[ ! -e $NOTESFILE ]]
then
    cp ${codedir}/analysis-template.txt $NOTESFILE
fi




######################################################################
# copy over the diagonal response matrices needed for spectral fitting

cp ${esas_caldb}/mos1-diag.rsp.gz ./analysis/
cp ${esas_caldb}/mos2-diag.rsp.gz ./analysis/
cp ${esas_caldb}/pn-diag.rsp.gz ./analysis/



cd $here
echo -e "\nodf directory prepared"
exit 0