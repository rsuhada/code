#!/bin/bash

######################################################################
# copies over the templates
# run before first module, it's independent of run-esaspi.sh at the
# price of hardcoded paths

obsid=$1
name=$2

if [[ $# == 1 ]]
then
    ######################################################################
    # try auto-greping a raw data file

    name=`grep ${obsid} ~/w/xspt/data/raw/data.txt | awk '{print $1}'`

fi

echo ${name} ${obsid}

# conf file
cp ~/data1/sw/esaspi/templates/template.conf configs/${name}.conf
sed -i "" "s/XXXXXXXXXX/${obsid}/g" configs/${name}.conf
sed -i "" "s/SPT-CL-JXXXX-XXXX/${name}/g" configs/${name}.conf

# modules file
cp ~/data1/sw/esaspi/templates/template.modules configs/${name}.modules


