This text file will guide you through the steps to running the code files in ME_341_Project

To start, just know that the Run_Abaqus.py code uses python2 to call Abaqus (2023 edition)
Similarly, the Abaqus_Figure_Maker.py is written in python2 and can be run directly in Abaqus

The Bayesian_Optimization.py, Random_Sample.py, and Plot_Maker.py programs use python3
Simply go to command window and type "python3 Bayesian_Optimization.py"
You can have Abaqus open to see the models being made each iteration, but don't run the ...
files through Abaqus directly. If you encounter an error with Abaqus open, then run the ...
code with Abaqus closed.

You'll have to install some of the imports used in the files; notable ones include
- pip install csv
- pip install pandas
- pip install numpy
- pip install matplotlib
- pip install odbaccess
- pip install scikit-optimize

To run Bayesian_Optimization.py:
- (line 97) make sure to set the path to abaqus.bat based on your path
- Change the number of iterations (line 129) and sample size (line 145) as desired

To run Random_Sample.py: 
- (line 55) make sure to set the path to abaqus.bat based on your path
- Change the number of iterations (line 156) as desired

For Plot_Maker.py:
- Set the read_csv function to read the name of the output files accordingly (lines 14-16)
- The plot setup requires 3 different csv files (from calling Bayesian_Optimization.py 3 times)
- Comment out all corresponding lines to data2 and data3 variables if testing only one csv file

For Plot_Maker.m:
- Same idea as in Plot_Maker.py

K-Fold_Cross_Validation.py:
- Same idea as in Plot_Maker.py
- Change values for n_cluster and n_folds as desired

If you want make multiple data sets, change the optimization_data.csv file name after each ...
completed run (the program rewrites the same csv file each run).

That should be all, hope this file was helpful!
