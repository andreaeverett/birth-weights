### Predicting Fetal Macrosomia

A blog post describing the project and results is available at https://andreaeverett.github.io/blog/Predicting_Birthweight/.

##### The code is contained in five Python files:
1. *'1_Import_Data'*: This file takes data from two fixed-width text files containing U.S. natality records for 2014 and 2015 and transforms them into 2 CSVs readable by Pandas (one for each year). The files are too large for upload to github, but can be downloaded [here](https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm) under 'U.S. Data (.zip files).' Reproducing the results will require the user to do this and run all five files in order, or to contact me directly for the data.

2. *'2_Reduce_size'*: This file opens the CSVs created in 1_Import_Data.py and eliminates all columns representing indicators for whether a given variable is reported by the state where the birth happened.  

3. *'3_Recode_missing'*: This file uses the reduced files from 2_Reduce_size.py and recodes all missing values. The value for missing data in most cases reflected the scale of the original variable, and so had to be calculated in a variety of different ways for different ones.

4. *'4_Apply_conditions'*: This file further reduces the data to the observations I chose to focus on for predicting birthweight: single, term, live births. It also drops cases where birthweight is missing.  The files remain too large (over 2 GB for each year) to upload.

5. *'5_Final_Results'*: This file contains code to produce the final model I summarize in the blog post and presentation, along with visualizations.

##### Other Files:
1. The 'Images' folder contains the graphs & visualizations produced in '5_Final_Results.'
2. 'Macrosomia_Presentation' contains the slides for a short presentation based on the results.
