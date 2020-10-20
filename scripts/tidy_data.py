"""
Written by Natalie Thurlby (email ask-jgi@bristol.ac.uk for help)

This script tidies the data that Usman sent to me (in .xlsx format) by:
* removing duplicate columns (the wavenumber for each sample), as it is the same for all samples
* giving one labelled row for columns (one wavenumber column, followed by sample names)
* saving it out as a csv (`tidy_data.csv`)
"""

import pandas as pd  # load the data manipulation library

df = pd.read_excel('../data.xlsx')

"""
After reading in the data we have something that looks like:

  T90_UT   Unnamed: 1 T90_T_A_10  ... Unnamed: 95 T90_T_UA_300_15 Unnamed: 97
0    wvn          abs        wvn  ...         abs             wvn         abs
1   4000  0.000113628       4000  ...       0.011            4000      0.0152
2   3999  9.56481e-05       3999  ...       0.011            3999      0.0151
3   3998   8.4668e-05       3998  ...       0.011            3998      0.0151
4   3997  7.86879e-05       3997  ...       0.011            3997      0.0151

What this means is that the column names are not correct for what they contain, e.g. the column "T90_UT" only contains 
the wave number, it is the column "Unnamed: 1" that contains the sample information.
"""

# Get list of column names:
sample_names = df.columns[df.columns.str.startswith('T')]  # column names corresponding to sample labels start with 'T'
unnamed_cols = df.columns[df.columns.str.startswith('U')]  # column names that start with 'U' (Unnamed)

# Delete all of the columns with sample names, except the first one (these all just contain the same wvn information):
df = df.drop(columns=list(sample_names.drop(sample_names[0])))

# Create a dictionary with keys for what we want to change from, and values for what we want to change to:
# (e.g. "Unnamed: 1": "T90_UT", "T90_UT":"wvn"), and use it to rename the columns:
column_mapping = {list(unnamed_cols)[i]: list(sample_names)[i] for i in range(len(sample_names))}
column_mapping[sample_names[0]] = 'wvn'
df = df.rename(columns=column_mapping)

# Set the "index" (row names) to be the wavenumber:
df = df.set_index('wvn')

# Delete the "wvn" row (which just contains either "abs" for all samples):
df = df.drop(index='wvn')

"""
Now we have something that looks like this:

           T90_UT   T90_T_A_10  ... T90_T_UA_300_14 T90_T_UA_300_15
wvn                             ...                                
4000  0.000113628 -4.92511e-05  ...           0.011          0.0152
3999  9.56481e-05 -3.16527e-05  ...           0.011          0.0151
3998   8.4668e-05  4.94583e-06  ...           0.011          0.0151
3997  7.86879e-05  5.75443e-05  ...           0.011          0.0151
3996  7.87078e-05  0.000105143  ...           0.011          0.0151

And I'm happy with that, so I save it as a .csv file.
"""

df.to_csv('../data/tidy_data.csv')
