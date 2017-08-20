import numpy as np
import pandas as pd


data = pd.read_excel('uniqnames_predict.xlsx')
o = data[['original_value']].values
o_list = []
for value in o:
	o_list.append(value[0])

p = data[['predict']].values
p_list = []
for value in p:
	p_list.append(value[0])	
a = np.corrcoef(o_list,p_list)

print(a)