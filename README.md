# Breakdown
Provides a powerful system to create weighted pivot tables, aggregations and reports.  
Leverages pandas for the groupby() function and general DataFrame utilities.  
Provides funcionality similar with pandas pivot_table but with the option to specify one or more weight fields using a custom data driven template.  
Its a implementation in pure python of the same system which is also available in [Perl](https://github.com/pemn/Namedtable) and [HTML5](https://github.com/pemn/ui_grid_breakdown)

## Features
 - Create pivot tables using weighted values.
 - Aggregation of values using a easy to assemble, plain text.
 - Very fast due to the numpy/pandas backend handling database I/O.
 - Small code base, leveraging already existing funcionality in the python ecosystem.
 - Template system compatible with my other implementations of this system (read above).
 - Built-in GUI using the libraries from my other project [usage-gui](https://github.com/pemn/usage-gui).
 - Command line arguments supported as a first-class citizen.

## Use cases
This system was created with support for generic csv files and also some specific database which are of little interest for the general public. Enough to say that any database that can be turned into a pandas DataFrame can be used as input.  

## Data driven template
The aggregation is defined by a template where each row defines a operation using a variable of the input table.  
The operations are:  
 - breakdown (default, group all values with this key)
 - mean (simple or weighted)
 - sum (simple or weighted)
 - min
 - max
 - count
 - major (TBI, present on other implementations of this system)
 - list (TBI)

## Example
Input:  

 | class1	 | class2	 | num1	 | num2	 | weight1	 | weight2	|
 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	|
 | A	 | C	 | 1	 | 1	 | 1	 | 1	|
 | A	 | C	 | 2	 | 1	 | 2	 | 2	|
 | A	 | D	 | 3	 | 2	 | 3	 | 1	|
 | A	 | D	 | 4	 | 2	 | 4	 | 2	|
 | B	 | E	 | 5	 | 3	 | 5	 | 1	|
 | B	 | E	 | 6	 | 3	 | 6	 | 2	|
 | B	 | F	 | 7	 | 4	 | 7	 | 1	|
 | B	 | F	 | 8	 | 4	 | 8	 | 2	|
 
 
Template:  
![template_grid](https://github.com/pemn/breakdown/blob/master/assets/asset1grid.png)  
Command Line (created automatically by the interface if desired):  
`python bm_breakdown.py breakdown_test.csv "" "class1,breakdown,;class2,breakdown,;num1,mean,;num2,mean,;num1=num1w1,mean,weight1;num2=num2w1,mean,weight1;num1,sum,;num2,sum,;num1=num1w1,sum,weight1;num2=num2w1,sum,weight1;num1=num1w1w2,mean,weight1,weight2;num2=num2w1w2,mean,weight1,weight2;num1=num1w1w2,sum,weight1,weight2;num2=num2w1w2,sum,weight1,weight2" breakdown_test_output.xlsx`

Output:  

 | class1	 | class2	 | num1	 | num2	 | num1w1	 | num2w1	 | num1	 | num2	 | num1w1	 | num2w1	 | num1w1w2	 | num2w1w2	 | num1w1w2	 | num2w1w2	|
 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	|
 | 	 | 	 | mean	 | mean	 | mean	 | mean	 | sum	 | sum	 | sum	 | sum	 | mean	 | mean	 | sum	 | sum	|
 | A	 | C	 | 1.5	 | 1	 | 1.66666666666667	 | 1	 | 3	 | 2	 | 5	 | 3	 | 1.8	 | 1	 | 9	 | 5	|
 | 	 | D	 | 3.5	 | 2	 | 3.57142857142857	 | 2	 | 7	 | 4	 | 25	 | 14	 | 3.72727272727273	 | 2	 | 41	 | 22	|
 | B	 | E	 | 5.5	 | 3	 | 5.54545454545455	 | 3	 | 11	 | 6	 | 61	 | 33	 | 5.70588235294118	 | 3	 | 97	 | 51	|
 | 	 | F	 | 7.5	 | 4	 | 7.53333333333333	 | 4	 | 15	 | 8	 | 113	 | 60	 | 7.69565217391304	 | 4	 | 177	 | 92	|


 

