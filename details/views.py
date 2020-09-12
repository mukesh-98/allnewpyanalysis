from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import math



#data1=pd.DataFrame()
# Create your views here.

def details(request):
    try : 
        if request.method== 'POST':
            NoApp=["NoApp"]
            NoUser=["NoUser"]
            data1=pd.DataFrame()
            file1 = request.FILES['file_1']
            if file1 != '':
                fs1=FileSystemStorage()
                name1=fs1.save(file1.name,file1)
                url1=fs1.url(name1)
                data1=pd.read_csv("."+url1)
                data1.reset_index(drop=True,inplace=True)
                forcol=pd.read_csv("./analysis/Tracking-2020-02-22.csv")
                if data1.columns.tolist() == forcol.columns.tolist():
                    data1=work(data1)
                    data1.to_csv('./static/dataframe.csv')
                    applist=data1['app_name'].unique().tolist()
                    userlist=data1['username'].unique().tolist()
                    return render(request,'details.html',{'file':str(file1),'data':data1,'app':applist,'user':userlist})
                else:
                    return render(request,'details.html',{'file':str("Invalid File"),'data':data1,'app':NoApp,'user':NoUser})
    except  : 
        return render(request,'home.html')

        
def work(data):
    # data=data.drop(['app_name','lat','lon','accelerometer'],axis=1)
        data=data.drop(['lat','lon'],axis=1)
        data.dropna(inplace=True)
        #df = pd.DataFrame(data['accelerometer_z']/np.sqrt(pow(data['accelerometer_x'],2)+pow(data['accelerometer_y'],2)+pow(data['accelerometer_z'],2)))
        #df.to_csv('file1.csv')
        data['Inclination'] = np.degrees(np.arccos(data['accelerometer_z']/np.sqrt(pow(data['accelerometer_x'],2)+pow(data['accelerometer_y'],2)+pow(data['accelerometer_z'],2))))
        data.dropna(inplace=True)
        data = data[data['username'] != 'swaptest']
        # Reading TimeStamp column and adding seperate time and date column
        temp = data['timestamp']
        temp1 = [x[11:] for x in temp]
        temp2 = [x[:10] for x in temp]
        year=[x[:4] for x in temp]
        month=[x[5:7] for x in temp]
        day=[x[8:10] for x in temp]
        time=[x[11:] for x in temp]
        data['year'],data['month'],data['day'],data['time']=(year,month,day,time)
        data['time'],data['Date']=(temp1,temp2)
        data['Day_name'] = pd.to_datetime(data['Date']).dt.day_name()
        data.drop([839,840],axis=0,inplace=True)
        return data
