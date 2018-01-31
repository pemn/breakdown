# Description
Provides a powerfull system to create weighted pivot tables and reports.  
Leverages pandas for the groupby() function and general DataFrame utilities.  
Provides funcionality similar with pandas pivot_table but with the option to specify one or more weight fields using a custom data driven template.

# How to use
This system was created with support for generic csv files and also some specific database which are of little interest for the general public. Enough to say that any database that can be turned into a pandas DataFrame can be used as input.

# Example
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
Output:  


 | class1	 | class2	 | num1	 | num2	 | num1w1	 | num2w1	 | num1	 | num2	 | num1w1	 | num2w1	 | num1w1w2	 | num2w1w2	 | num1w1w2	 | num2w1w2	|
 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	 | ---	|
 | A	 | C	 | 1.5	 | 1	 | 1.66666666666666	 | 1	 | 3	 | 2	 | 5	 | 3	 | 1.8	 | 1	 | 9	 | 5	|
 | A	 | D	 | 3.5	 | 2	 | 3.57142857142857	 | 2	 | 7	 | 4	 | 25	 | 14	 | 3.72727272727272	 | 2	 | 41	 | 22	|
 | B	 | E	 | 5.5	 | 3	 | 5.54545454545454	 | 3	 | 11	 | 6	 | 61	 | 33	 | 5.70588235294117	 | 3	 | 97	 | 51	|
 | B	 | F	 | 7.5	 | 4	 | 7.53333333333333	 | 4	 | 15	 | 8	 | 113	 | 60	 | 7.69565217391304	 | 4	 | 177	 | 92	|
 
 
 

