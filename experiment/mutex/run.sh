#! /bin/bash
host=`hostname -s`
test_file=test.maude

for node in `cat node`
do
    for bias in `cat bias`
    do
	    conf="$node-$bias-median"
        echo $conf
	    python gen.py test.maude.temp test.maude $node $bias
		echo `date`
	    java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f median.quatex -a 0.05 > ${host}-$conf.out 2>&1
	    result=`python result.py ${host}-$conf.out`
	    echo $conf $result
	    echo $conf $result >> result.out
    done
done

for node in `cat node`
do
    for bias in `cat bias`
    do
	    conf="$node-$bias-longestWait"
        echo $conf
	    python gen.py test.maude.temp test.maude $node $bias
		echo `date`
	    java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f longestWait.quatex -a 0.05 > ${host}-$conf.out 2>&1
	    result=`python result.py ${host}-$conf.out`
	    echo $conf $result
	    echo $conf $result >> result.out
    done
done

for node in `cat node`
do
    for bias in `cat bias`
    do
	    conf="$node-$bias-avgWait"
        echo $conf
	    python gen.py test.maude.temp test.maude $node $bias
		echo `date`
	    java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f avgWait.quatex -a 0.05 > ${host}-$conf.out 2>&1
	    result=`python result.py ${host}-$conf.out`
	    echo $conf $result
	    echo $conf $result >> result.out
    done
done
