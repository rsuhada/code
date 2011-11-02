######################################################################
# NOTE: not very useful at the moment - but contains the solution to
# the xspec bus error problem (see notes.txt)

######################################################################
# task to unset the SAS parameters

unset SAS_DIR
unset SAS_PATH
unset SAS_CCFPATH
unset SAS_MEMORY_MODEL
unset SAS_VERBOSITY
unset SAS_ODF
unset SAS_CCF


######################################################################
# the xspec workaround due to heasas vs. sas11 conflict

echo $DYLD_LIBRARY_PATH
echo
echo
export DYLD_LIBRARY_PATH=/Users/rs/data1/sw/heasoft-6.11/i386-apple-darwin10.7.0/lib
echo $DYLD_LIBRARY_PATH
echo
echo