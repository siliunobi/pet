#!/bin/bash
host=`hostname -s`
test_file=test.maude

#metric="latency"
metric="throughput"
#for loads in 180 100 ;
for loads in 190 ;
do
	for cls in 20 40 60 80 100 ;
	do
		for rlevel in "one" "quorum" "all" ;
		do
			conf="$metric-$loads-$cls-$rlevel"
			
			metric_file="throughput.quatex"
			if [ $metric = 'latency' ];
			then
				metric_file="avglatency.quatex"
			fi

			echo $conf $metric_file

			python gen.py test.maude.temp test.maude $loads $cls $rlevel
			echo `date`
			java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f ${metric_file} -a 0.05 > ${host}-$conf.out 2>&1
			result=`python result.py ${host}-$conf.out`
			echo $conf $result
			echo $conf $result >> result.out
		done
	done
done

