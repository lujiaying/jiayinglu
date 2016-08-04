import pandas as pd
import numpy as np
from sklearn.datasets import dump_svmlight_file

"""
Source from https://www.kaggle.com/c/telstra-recruiting-network/forums/t/18223/python-is-there-any-elegant-way-to-convert-dataframe-to-libsvm-format
"""

df = pd.DataFrame()
df['Id'] = np.arange(10)
df['F1'] = np.random.rand(10,)
df['F2'] = np.random.rand(10,)
df['Target'] = map(lambda x: -1 if x < 0.5 else 1, np.random.rand(10,))

X = df[np.setdiff1d(df.columns,['Id','Target'])]
y = df.Target

print df

dump_svmlight_file(X,y,'smvlight.dat',zero_based=True,multilabel=False)
