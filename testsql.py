import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import matplotlib.pyplot as plt
#from sklearn.linear_model import LinearRegression
import numpy as np
np.set_printoptions(threshold=np.inf)
import pandas as pd
from pandas import ExcelWriter


db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="jubi",  # your password
                     db="parsed")



cursor = db.cursor()

def getQueryResult(query):
    result = pd.read_sql(query, db)
    return result



data = getQueryResult('select report.name,report.gender,report.age,report.report_id, test.name, test.value from report join profile on report.report_id=profile.report_report_id join test on test.profile_profile_id=profile.profile_id where report.report_id in (select profile.report_report_id from profile where profile.name = "kidney" and profile.report_report_id in ( select profile.report_report_id from profile where name = "cholesterol" and profile.report_report_id in ( select profile.report_report_id from profile where name = "diabetes"))) and (test.name like "%CREATININE - SERUM%" or test.name like "%BLOOD UREA NITROGEN (BUN)%" or test.name like "%LDL / HDL RATIO CALCULATED%" or test.name like "%HbA1c%");')

report_id = data[["report_id"]].values
name = data.iloc[:,0].values
test_name = data.iloc[:,4].values
test_value = data[['value']].values
gender = data[['gender']].values
age = data[['age']].values

# data_2 = pd.Dataframe({'report_id':,'name':,'age': ,'t1':,'v1':,'t2':,'v2':,'t3':,'v3':,'t4':,'v4':})

data2 = data.set_index("report_id")
r_id = np.unique(report_id)
age_list = []
data_list =[]
for rid in r_id:
    d = {'id':'','name':'','gender':'','t1':'','bun_value':0,'t2':'','creat_value':0,'t3':'','cho_ratio_value':0,'t4':'','hba1c_value':0}
    df = data2.loc[rid,:]
    d['id'] = rid
    try:
        for row in df.iterrows():
            d['name'] =row[1].iloc[0]
            
            d['gender'] = row[1]['gender']
            if "HbA1c" in row[1].iloc[3]:
                d['t4'] = row[1].iloc[3]
                d['hba1c_value'] = row[1]['value']
            if "CREATININE - SERUM" in row[1].iloc[3]:
                d['t2'] = row[1].iloc[3]
                d['creat_value'] = row[1]['value']
            if "BLOOD UREA NITROGEN (BUN)" in row[1].iloc[3]:
                d['t1'] = row[1].iloc[3]
                d['bun_value'] = row[1]['value'] 
            if "LDL / HDL RATIO CALCULATED" in row[1].iloc[3]:
                d['t3'] = row[1].iloc[3]
                d['cho_ratio_value'] = row[1]['value']
            
    except AttributeError:
        continue
    if d['cho_ratio_value']==0 or d['bun_value']==0 or d['creat_value']==0 or d['hba1c_value']==0 :
        print('0')
    else:  
        age_list.append(row[1]['age'])  
        data_list.append(d)



clean_data = pd.DataFrame(data_list)
clean_data['age'] = age_list
writer = ExcelWriter('data_set.xlsx')
clean_data.to_excel(writer,'Sheet1')
writer.save()