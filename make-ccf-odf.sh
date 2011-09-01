######################################################################
# run odfingest and ccf

dir=$1
here=`pwd`
cd $dir


######################################################################
# make ccf

echo -e "\nStarting CCF creation :\n"

cifbuild withccfpath=no analysisdate=now category=XMMCCF calindexset=$SAS_CCF fullpath=yes verbosity=4

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: cifbuild failed !"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi

echo -e "\nCCF file : "
ls ${SAS_CCF}/ccf.cif


######################################################################
# make odf

echo -e "\nStarting ODF ingestion :\n"
odfingest odfdir=$SAS_ODF outdir=$SAS_ODF verbosity=4

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: odfingest failed !"
    echo -e "*** error in script: $0\n"
    cd $startdir
    exit 1
fi

echo -e "\nODF file : "
ls ${SAS_ODF}/*SUM.SAS

######################################################################
# exit

cd $here
echo -e "\n$0 in $obsid done!"
exit 0