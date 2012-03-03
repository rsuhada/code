#!/bin/bash

logfile=$1

echo "######################################################################"
echo "TASK is designed to find SAS errors only"
echo "the list of other errors might be incomplete!"
echo "######################################################################"
echo "Warnings:"
echo

egrep -in "\*\*" $logfile | egrep -iv ".\*\*2" | grep -iv error | grep -iv badpixfind | egrep -iv "Limit.* CCD=.* Hardness=.* Uncertainty=.*"  | egrep -iv "grppha .* completed successfully" | egrep -iv "Program completed successfully"

echo
echo "######################################################################"
echo "Errors:"
echo

egrep -in "\*\*" $logfile | egrep -iv ".\*\*2" | grep -iv warning | grep -iv badpixfind | egrep -iv "Limit.* CCD=.* Hardness=.* Uncertainty=.*" | egrep -iv "grppha .* completed successfully" | egrep -iv "Program completed successfully"