echo "Start to generate files"
python step1.py $@

echo "Run maude"
maude full-maude/pmonitor.maude > output 

echo "Start to extract output and replace"
python step2.py $@

if [ "$2" = "on" ];
then
    echo "run pvesta"
	java -jar pvesta/pvesta-client.jar -l pvesta/${12} -m test.maude -f $9 -a ${10} -d1 ${11} > smc-result &
fi

echo "Done"
