dir=$1

mv [p,m]?-${dir}.* ${dir}/

echo cp ${specdir}/${PS_REGION_ID}.im.reg ${dir}/
cp ${bgspecdir}/${PS_REGION_ID}.im.reg ${dir}/
