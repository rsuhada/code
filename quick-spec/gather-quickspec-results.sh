######################################################################
# collect the files written by a xspec driver script into a directory

if [[ $# == 0 ]]
then
    echo "missing parameters:"
    echo "gather-quickspec-results.sh directory_name [OVERWRITE_FLAG 1/0]"
    exit 1
fi

dir=$1
OVERWRITE=$2

if [[ ! -e $dir || $OVERWRITE -eq 1 ]]
then
    mkdir $dir

    mv *.xspec            ${dir}/
    mv *.result           ${dir}/
    mv *uf.ps             ${dir}/
    mv *nice.ps           ${dir}/
    mv *nice.png          ${dir}/
    mv *data.ps           ${dir}/
    mv *model.xcm         ${dir}/
    mv *session.log       ${dir}/
    mv *fx-lx.log         ${dir}/
    mv *fx-lx-err.log     ${dir}/
    mv *gof.log           ${dir}/
    mv *err.log           ${dir}/
    mv *contour.ps        ${dir}/

    echo
    echo "Results gathered in: " $dir
    echo
else
    echo "Dir :: " $dir
    echo "** ERROR: already exists"
    echo
fi


