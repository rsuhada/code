dir=$1

if [[ ! -e $dir ]]
then
    mkdir $dir

    mv *.xspec         ${dir}/
    mv *.result        ${dir}/
    mv *-uf.ps         ${dir}/
    mv *-nice.ps       ${dir}/
    mv *-data.ps       ${dir}/
    mv *-model.xcm     ${dir}/
    mv *-session.log   ${dir}/
    mv *-gof.log       ${dir}/
    mv *-err.log       ${dir}/
    mv *-contour.ps    ${dir}/
    mv *-fx-lx.log     ${dir}/

    echo
    echo "Results gathered in: " $dir
    echo
else
    echo "Dir :: " $dir
    echo "** ERROR: already exists"
    echo
fi


