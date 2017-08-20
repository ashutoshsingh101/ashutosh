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

# data_2 = pd.Dataframe({'report_id':,'name':,'age': ,'t1':,'v1':,'t2':,'v2':,'t3':,'v3':,'t4':,'v4':})

data2 = data.set_index("report_id")
r_id = np.unique(report_id)
d = {'id':[],'name':[],'age': 0,'gender':[],'t1':[],'bun_value':0,'t2':[],'creat_value':0,'t3':[],'cho_ratio_value':0,'t4':[],'hba1c_value':0}
h_name = []
c_name = []
bun_name = []
cho_name = []

h_value = []
c_value = []
bun_value = []
cho_value = []

name_l = []
age_l = []
gender_l = []

id_list = []

for rid in r_id:
    
    df = data2.loc[rid,:]
    id_list.append(rid)
    try:
        for row in df.iterrows():
            name_l.append(row[1].iloc[0])
            age_l.append(row[1]['age'])
            gender_l.append(row[1]['gender'])
            if "HbA1c" in row[1].iloc[3]:
                h_name.append(row[1].iloc[3])
                h_value.append(row[1]['value'])
            if "CREATININE - SERUM" in row[1].iloc[3]:
                c_name.append(row[1].iloc[3])
                c_value.append(row[1]['value'])
            if "BLOOD UREA NITROGEN (BUN)" in row[1].iloc[3]:
                bun_name.append(row[1].iloc[3])
                bun_value.append(row[1]['value'])
            if "LDL / HDL RATIO CALCULATED" in row[1].iloc[3]:
                cho_name.append(row[1].iloc[3])
                cho_value.append(row[1]['value'])
            
    except AttributeError:
        continue
    if row[1]['value']==0:
        print('0')
    else:
    	d = {'id':id_list,'name':name_l,'age':age_l,'gender':gender_l,'t1':bun_name,'bun_value':bun_value,'t2':c_name,'creat_value':c_value,'t3':cho_name,'cho_ratio_value':cho_value,'t4':h_name,'hba1c_value':h_value}   
        

clean_data = pd.DataFrame(data=d)
writer = ExcelWriter('data_set_2.xlsx')
clean_data.to_excel(writer,'Sheet1')
writer.save()