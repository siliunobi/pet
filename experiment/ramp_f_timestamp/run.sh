#! /bin/bash
host=`hostname -s`
test_file=test.maude

rm result.out
for dist in `cat dist`
do
    for load in `cat load`
    do
        for key in `cat keys`
        do
	    conf="$load-$key-$dist-2-2-10"
            echo $conf
	    python gen.py test.maude.temp test.maude $load 10 $key  $dist 2 2
		echo `date`
	    java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f pf.quatex -a 0.05 > ${host}-$conf.out 2>&1
	    result=`python result.py ${host}-$conf.out`
	    echo $conf $result
	    echo $conf $result >> result.out
        done
    done
done

for dist in `cat dist`
do
    for load in `cat load`
    do
        for key in `cat keys`
        do
	    conf="$load-$key-$dist-2-2-30"
            echo $conf
	    python gen.py test.maude.temp test.maude $load 30 $key  $dist 2 2
	    java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f pf.quatex -a 0.05 > ${host}-$conf.out 2>&1
	    result=`python result.py ${host}-$conf.out`
	    echo $conf $result
	    echo $conf $result >> result.out
        done
    done
done

for dist in `cat dist`
do
    for load in `cat load`
    do
        for key in `cat keys`
        do
	    conf="$load-$key-$dist-2-2-50"
            echo $conf
	    python gen.py test.maude.temp test.maude $load 50 $key  $dist 2 2
	    java -jar ~/pvesta/pvesta-client.jar -l ~/pvesta/serverlist1 -m ${test_file} -f pf.quatex -a 0.05 > ${host}-$conf.out 2>&1
	    result=`python result.py ${host}-$conf.out`
	    echo $conf $result
	    echo $conf $result >> result.out
        done
    done
done
