######################################################################
# script links rmf and arf files from a target directory
# useful for iter-spec if you don'the want to calculate you

dir=$1

if [[ $# == 0 ]]
then
    echo -e "** error: missing directory with the arf/rmf files"
    echo -e "*** file naming has to be of form: pn-*.rmf etc."
    exit 0
fi

ln -s ${dir}/pn-*.rmf pn.rmf
ln -s ${dir}/m1-*.rmf m1.rmf
ln -s ${dir}/m2-*.rmf m2.rmf

ln -s ${dir}/pn-*.arf pn.arf
ln -s ${dir}/m1-*.arf m1.arf
ln -s ${dir}/m2-*.arf m2.arf

