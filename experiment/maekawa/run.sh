#! /bin/bash
host=`hostname -s`
test_file=test.maude

for node in `cat node`
do
	    conf="$node"
        echo $conf
	    python gen.py test.maude.temp test.maude $node
		echo `date`
	    java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f deadlock.quatex -a 0.05 > ${host}-$conf.out 2>&1
	    result=`python result.py ${host}-$conf.out`
	    echo $conf $result
	    echo $conf $result >> result.out
done
