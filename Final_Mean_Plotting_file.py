import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import statsmodels.api as sm


conn = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="jubi",
                     db="parsed")
def getQueryResult(query):
    result = pd.read_sql(query, conn)
    return result



columns = ['report_id','age']
important_test_names = ['HbA1c','LDL / HDL RATIO CALCULATED','CREATININE - SERUM']
columns.extend(important_test_names)
master = pd.DataFrame(columns=columns)

report_list = getQueryResult('select distinct report.report_id from report join profile on report.report_id = profile.report_report_id join test on profile.profile_id = test.profile_profile_id;')

for i in range(len(report_list)):
    rID_info = {}
    
    rID_info['age'] = getQueryResult('select report.age from report where report.report_id =\''+str(report_list.iloc[i][0])+'\';').loc[0][0]
    rID_info['report_id'] = str(report_list.iloc[i][0])
    
    for tests in important_test_names:
        reportIDInfo = getQueryResult('select report.report_id, test.name, test.value from report join profile on report.report_id = profile.report_report_id join test on profile.profile_id = test.profile_profile_id where test.name = \''+tests+'\' and report.report_id = \''+str(report_list.iloc[i][0])+'\';')    

        if not reportIDInfo.empty:
            name  = str(reportIDInfo.iloc[0][1]).strip()
            try:
                value = float(str(reportIDInfo.iloc[0][2]).strip())
            except ValueError:
                print('blah '+str(reportIDInfo.iloc[0][2]).strip()+' '+str(name)+' '+str(report_list.iloc[i][0]))
                continue
            rID_info[name] = value
    
    
    result = []
    
    for col in columns:
        try:
            blah = rID_info[col.strip()]
            
            result.append(blah)
        except:
            result.append(np.nan)
            continue
    
    master.loc[master.shape[0]] = result
    
    del(rID_info)

listAge = list(range(100)) #age can only be in the range zero to 100


# In[16]:


def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0 else x for x in values]



def getMeanForEach(testName):
    # This method returns the mean of the test values for each age specified in the data. 
    # For an age where there is no datapoint, it return zero in the returned list
    
    age_VS_hba = master[['age', testName]] #get the required columns
    age_VS_hba.sort_values(by='age')
    
    plotting_dict = {}

    for i, row in age_VS_hba.iterrows():

        tupl = (0,0)
        age = age_VS_hba.loc[i, 'age']
        value = age_VS_hba.loc[i, testName]

        if age in plotting_dict:
            tupl = plotting_dict[age]
            #print('tuple is '+str(tupl[0]),str(tupl[1])+' for age '+age)
        
        if not math.isnan(value):
            tupl = (tupl[0] + 1, tupl[1] + value)

        plotting_dict[age] = tupl
        
        #----------------------------------
    
    result_dict = [0] * 100 #init array of zeros
    
    plotting_dict.pop('', None) #unclean data. one entry exists where there is no age
    
    for key in plotting_dict:
        #key is the age
        
        #print('age: '+str(key)+' count: '+str(plotting_dict[key][0])+' value: '+str(plotting_dict[key][1]))
        
        if float(plotting_dict[key][0]) != 0:
            result_dict[int(key)] = float("{0:.2f}".format(float(plotting_dict[key][1]) / float(plotting_dict[key][0]))) #store mean value in result_dict for each age
        
    
    del(plotting_dict)
    #print('\n output from getMeanForEach: ')
    print(result_dict)
    
    # we shall return a list where each index holds the mean value at that age.
    return result_dict



def makeTupleWithIndex(listX):
    '''
    takes in a list, returns a list of tuples made by joining the list elements with their index. 
    example, age vs. mean values at that age.
    input can be something like a list with mean values at each index where index is the age.
    '''
    result = [0]*100
    for index in range(len(listX)):
        result[index] = (index, listX[index])
        # tuple has (age, mean value)
        
    return result




def normalise(list_input):
    #normalises to a range 0 to 1
    return [float(i)/sum(list_input) for i in list_input]



def drawGraphForTest(testName):
    plotting_list = getMeanForEach(testName)
    plottting_list = [i for i in plotting_list if i > 0.0]
    
    #plt.ylim(ymin = 0.001)
    # plt.scatter(listAge, plotting_list, color='blue')
    # plt.xlabel('age')
    # plt.ylabel(str(testName)+' value')
    # plt.grid()
    #plt.savefig('p'+str(index)+'.png',type = 'png')
    #plt.show()
    return plotting_list


hba1c = drawGraphForTest('HbA1c')
cholesterol_ratio = drawGraphForTest('LDL / HDL RATIO CALCULATED')
creatinine = drawGraphForTest('CREATININE - SERUM')





data = pd.DataFrame({'x':listAge,'y':cholesterol_ratio, 'z':creatinine,'p':hba1c})

X = data[['x','y','z']]
Y = data[['p']]


X_train = X.loc[20:70,:]
Y_train = Y.loc[20:70,:]
X_test = X.loc[70:80,:]
Y_test = Y.loc[70:80,:]
X1_train = sm.add_constant(X_train)
X1_test = sm.add_constant(X1_test)
est = sm.OLS(Y_train,X1_tain).fit()
print(est.summary())
print(est._results.params)

predictions = est.predict(X1_test)


