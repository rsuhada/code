######################################################################
# run emchains and epchains

dir=$1
here=`pwd`
cd $dir


######################################################################
# make ccf
echo -e "\nRunning event calibration chains :"

# pn
epchain verbosity=1

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: epchain failed!"
    echo -e "error in script: $0\n"
    cd $startdir
    exit 1
fi

# pn oot
epchain withoutoftime=true verbosity=1

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: epchain OOT failed!"
    echo -e "error in script: $0\n"
    cd $startdir
    exit 1
fi

# mos
emchain verbosity=1

if [[ $? -ne 0 ]]
then
    echo -e "\n** error: emchain failed!"
    echo -e "error in script: $0\n"
    cd $startdir
    exit 1
fi


######################################################################
# exit
cd $here
echo -e "\n$0 in $obsid done!"
exit 0