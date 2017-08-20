import statsmodels.api as sm
import pandas as pd
from pandas import ExcelWriter
import matplotlib.pyplot as plt
import numpy as np




data = pd.read_excel('dropna.xlsx')

age_list = data[['age']].values
ages=[]

for age in age_list:
	ages.append(age[0])


data['gender_code'] = pd.Categorical(data.gender).codes
# data['age_norm'] = data['age'].apply(lambda x: int(str(x)))

df = data.set_index("name")
# uniqnames = df[np.unique(df["name"])]        
uniqnames = df.groupby(level=0).first()

mean_c = np.mean(uniqnames['cho_ratio_value'].values)
den_c = np.amax(uniqnames['cho_ratio_value'].values) - np.amin(uniqnames['cho_ratio_value'].values)
uniqnames['cho_ratio_value'] = uniqnames['cho_ratio_value'].apply(lambda x: (x-mean_c)/den_c)

mean_cr = np.mean(uniqnames['creat_value'].values)
den_cr = np.amax(uniqnames['creat_value'].values) - np.amin(uniqnames['creat_value'].values)
uniqnames['creat_value'] = uniqnames['creat_value'].apply(lambda x: (x-mean_cr)/den_cr)

mean_b = np.mean(uniqnames['bun_value'].values)
den_b = np.amax(uniqnames['bun_value'].values) - np.amin(uniqnames['bun_value'].values)
uniqnames['bun_value'] = uniqnames['bun_value'].apply(lambda x: (x-mean_b)/den_b)

mean_a = np.mean(uniqnames['age'].values)
den_a = np.amax(uniqnames['age'].values) - np.amin(uniqnames['age'].values)
uniqnames['age'] = uniqnames['age'].apply(lambda x: (x-mean_a)/den_a)

# mean_g = np.mean(uniqnames['gender_code'].values)
# den_g = np.amax(uniqnames['gender_code'].values) - np.amin(uniqnames['gender_code'].values)
# uniqnames['gender_code'] = uniqnames['gender_code'].apply(lambda x: (x-mean_g)/den_g)

mean_h = np.mean(uniqnames['hba1c_value'].values)
den_h = np.amax(uniqnames['hba1c_value'].values) - np.amin(uniqnames['hba1c_value'].values)
uniqnames['hba1c_value'] = uniqnames['hba1c_value'].apply(lambda x: (x-mean_h)/den_h)

#total samples separated
X_total = uniqnames[['cho_ratio_value','creat_value','bun_value','age','gender_code']]
Y_total = uniqnames[['hba1c_value']]

#total samples after filterin diabetes values
total_test = uniqnames[np.logical_and(uniqnames.hba1c_value>=-0.085,uniqnames.hba1c_value<=.098)]
y_total_test = total_test[['hba1c_value']].apply(lambda x: (x*den_h) + mean_h)
x_total_test =  total_test[['cho_ratio_value','creat_value','bun_value','age','gender_code']]





X_train = X_total.iloc[0:6200,:]
# X_test = X_total.iloc[6200:,:]
Y_train = Y_total.iloc[0:6200,:]
# Y_test = Y_total.iloc[6200:,:]

# Y_test[['hba1c_value']] = Y_test[['hba1c_value']].apply(lambda x: (x*den_h) + mean_h)









y_t = y_total_test[['hba1c_value']].values
y_test = []
for value in y_t:
	y_test.append(value[0])



X1_train = sm.add_constant(X_train)
X1_test = sm.add_constant(x_total_test)
est = sm.OLS(Y_train,X1_train).fit()
print(est.summary())
print(est._results.params)


predictions = est.predict(X1_test)
predictions = predictions.apply(lambda x: (x*den_h) + mean_h)

predicted_values= predictions.values



error = []
for i in range(len(predicted_values)):
	err= (y_test[i] - predicted_values[i])
	error.append(err)

correct = 0
incorrect = 0

for e in error:
	if abs(e) <= .6:
		correct = correct +1

acc = float(float(correct)/float(len(error)))
print(acc*100)


fig = plt.figure(figsize=(11,11))
plt.scatter(y_test,predicted_values,label='accuracy = 65%')
x = np.linspace(3, 9, 1000)
plt.plot(x,x,color = 'red',label='error nmargin = 0.6')
plt.legend(loc='upper left')
plt.xlabel('original_values')
plt.ylabel('predicted_values')
plt.title('relationship between real and predicted values')
plt.xlim((3,9))
plt.ylim((3,9))


plt.savefig('predictions_uniqnmaes.png',type= 'png')

predic = pd.DataFrame({'original_value':y_test,'predict':predictions,'errors':error})
writer = ExcelWriter('uniqnames_predict.xlsx')
predic.to_excel(writer,'Sheet2')
writer.save()

