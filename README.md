# Performance Estimation Tool (PET)

This project is a tool for transforming a Maude specification into a new one which can be model checked by Maude statistic model checker. 

How to use:

1. Go to the folder where your target Maude spec is located. 
2. load autoTag.maude  into Maude (make sure full-maude is in the same folder or the folder Maude can find it)
3. load target Maude file 
4. Use the command (monitor ModuleName .) to perform transformation 
5. Use the command (show module ModuleName .) to output the spec. 


