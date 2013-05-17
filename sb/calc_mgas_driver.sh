# FIXME: add run-esas interface
# FIXME: install lmgit to 2.7 and use the newer python!
export PYTHONEXEC=/usr/bin/python2.6
export codedir="/Users/rs/data1/sw/esaspi"

# cluster settings

source /Users/rs/w/xspt/data/dev/0559/sb/calc_mgas.conf

echo $PYTHONEXEC ${codedir}/py/test/calc_mgas_cluster.py $z $r500 $trad_fname $fitted_pars_file $TEST_MODEL_NAME
$PYTHONEXEC ${codedir}/py/test/calc_mgas_cluster.py $z $r500 $trad_fname $fitted_pars_file $TEST_MODEL_NAME