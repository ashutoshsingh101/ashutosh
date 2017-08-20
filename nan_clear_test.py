import pandas as pd
from pandas import ExcelWriter
import numpy as np


data = pd.read_excel('data_set.xlsx')

df = data.dropna()
# df = data[np.isfinite(data['age'])]

writer = ExcelWriter('dropna.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()