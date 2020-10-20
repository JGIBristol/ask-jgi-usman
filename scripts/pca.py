"""
This script:
 - loads in our tidy data (created using `tidy_data.py`)
 - transposes it (PCA module assumes columns = dimensions to reduce)
 - performs PCA
    - checks and prints variance explained
    - transforms data into space of 2 principal components
 - creates an interactive plot using plot.ly
"""

import pandas as pd  # for data manipulation
import sklearn.decomposition.pca as pca  # for PCA
import plotly.express as px  # for interactive plots

# READ IN DATA:
df = pd.read_csv('../data/tidy_data.csv', index_col='wvn')

# PCA:
n_components = 2  # Number of principal components to reduce to.
df = df.transpose()
pca = pca.PCA(n_components=n_components)
fit = pca.fit(df)
transformed = pca.transform(df)

# Variance explained:
print(sum(pca.explained_variance_))

# Plot figure:
fig = px.scatter(x=transformed[:, 0],
                 y=transformed[:, 1],
                 text=list(df.index),
                 labels={'x': 'Principal component 1', 'y': 'Principal component 2'})
fig.update_traces(mode="markers")  # this line means text is displayed on hover, not all the time.
fig.show()
