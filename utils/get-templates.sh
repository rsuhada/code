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

    name=`grep ${obsid} ~/w/xspt/data/raw/data.txt | awk '{print $1}' | tail -1`

fi

echo ${name} ${obsid}

# conf file
# CHANGE PATH
cp ~/data1/sw/esaspi/templates/template.conf configs/${name}.conf
sed -i.bk "s/1XXXXXXXXXX/${obsid}/g" configs/${name}.conf ; rm configs/${name}.conf.bk
sed -i.bk "s/2XXXXXXXXXXXXXXXXX/${name}/g" configs/${name}.conf ; rm configs/${name}.conf.bk

# modules file
# CHANGE PATH
cp ~/data1/sw/esaspi/templates/template.modules configs/${name}.modules

# the analysis file: note that it might be rewriten by prep-odf-dir.sh and/or can have a different name as defined by $NOTESFILE in the main pipe
