dir=$1

mv [p,m]?-${dir}.* ${dir}/
mv cluster-iter-r-${rpad}.wcs.reg ${dir}/
mv cluster-iter-r-${rpad}.phy.reg ${dir}/
mv cluster-iter-rcore-r-${rpad}.wcs.reg ${dir}/
mv cluster-iter-rcore-r-${rpad}.phy.reg ${dir}/
mv *${dir}*.fpars ${dir}/

cp ${PS_REGION_ID}.im.reg ${dir}/

rm *${rpad}*.desc
