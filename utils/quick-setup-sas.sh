######################################################################
# a auxiliary script to setup sas for task that want to run outside
# the run-esaspi.sh script

odfdir=$1
ccfdir=$2

export codedir="/Users/rs/data1/sw/esaspi"
export esas_caldb="/Users/rs/calib/esas"

export SAS_DIR="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
export SAS_PATH="/Users/rs/data1/sw/sas-11.0.0/xmmsas_20110223_1803"
export SAS_CCFPATH="/Users/rs/calib/xmm/ccf/"
export SAS_MEMORY_MODEL=high
export SAS_VERBOSITY=4

export SAS_ODF=${odfdir}
export SAS_CCF=${ccfdir}/ccf.cif

sasversion

