# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 17:38:56 2020

@author: Rajiv
"""
'''
['Basic_Electrical_Engineering_AR' 'Engineering_Mechanics_AR'
 'Engineering_Drawing_AR' 'Drone_Fundamentals' nan
 'Drone_Flying_Fundamentals' 'demoapp']

'''
from collections import Counter
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import re
from sklearn.linear_model import LinearRegression
import sklearn.cluster as cluster
from analysis import analysisfile as an
from details import views as details

#appdata = pd.read_csv("Tracking-2020-02-22.csv")
#print(appdata['app_name'].unique())
#optimaltotal = pd.Timedelta(0)
appname = "Drone_Fundamentals"

#Reading and dropping unused columns and NaN values
#data = pd.read_csv("Tracking-2020-02-22.csv")
#temp=data.drop(["accelerometer_x","accelerometer_x","accelerometer_y","accelerometer_z","lon","lat"],axis=1)
#temp=temp.dropna()


#Segregating through user name then app name to pinpoint drone fundamentals and junaid user
#for user,data in temp.groupby(['username']):
#    if user=="junaid":
#        for app,data1 in data.groupby(['app_name']):
#            if app==appname:
#                break
#if appname == "Drone_Fundamentals":
#    data1 = data1.drop(data1.loc[746:].index)


#segregating timestamps into multiple column
#temp = data1['timestamp']
#temp1 = [x[11:] for x in temp]
#temp2 = [x[:10] for x in temp]
#data1['time'],data1['Date']=(temp1,temp2)
#data1['Day_name'] = pd.to_datetime(data1['Date']).dt.day_name()

'''Changes made above : segregated to drone fundamentals and to junaid user , removed wrong entries'''


''' DO NOT TOUCH   '''
#data=data1
#firsttime = pd.to_datetime(data.iloc[0]['timestamp'])
#lasttime = pd.to_datetime(data.iloc[1]['timestamp'])
#diff=abs(firsttime-lasttime)
#print(diff)


'''   Start from here   '''
#calculating time for each step by ideal user
#timeDiff=[]
#for i in range(len(data['id'])-1,0,-1):
#    firstime = pd.to_datetime(data.iloc[i]['timestamp'])
#    lastime = pd.to_datetime(data.iloc[i-1]['timestamp'])
#    timeDiff.append(abs(firstime-lastime))
#minLength = len(data)

#for i in timeDiff:
#    optimaltotal += i

#extracting and refining 10 normal users

X=details.x
y=details.y


data2 = pd.read_csv("."+X)
scoreSampleFile =pd.read_csv("."+y)


data2=data2.drop(["accelerometer_x","accelerometer_x","accelerometer_y","accelerometer_z","lon","lat"],axis=1)
data2=data2.dropna()

#Extracting enteries only for "drone fundamentals" app
#for app,data2 in data2.groupby(['app_name']):
#    if app==appname:
#        break
#Removing "junaid"(ideal user) entries
data2=data2.drop(data2.index[data2['username']=="junaid"].tolist())
normalUsers = data2['username'].unique().tolist() #list of all the unique users excluding ideal user

#removes all the test users (may require multiple passes )
'''if appname == "Drone_Fundamentals":
    for i in normalUsers:
        if not re.search("^drone",i):
            normalUsers.pop(normalUsers.index(i))'''


#logic for getting time required for each normal user for each step
normalUserDiff = {}
temp=[]
for uniqueUser in normalUsers:
    for user,data3 in data2.groupby(['username']):
        if user==uniqueUser:
            break
    for i in range(len(data3['id'])-1,0,-1):
        firstime = pd.to_datetime(data3.iloc[i]['timestamp'])
        lastime = pd.to_datetime(data3.iloc[i-1]['timestamp'])
        temp.append(abs(firstime-lastime))
    normalUserDiff[uniqueUser]=temp
    temp=[]


l111 = []
l222 = []
l333 = []

timetotallist = []
#scoreSampleFile = pd.read_csv('scoreSampleFile.csv')
for i in range(len(scoreSampleFile)):
    timetotallist = list(normalUserDiff[scoreSampleFile.iloc[i]['user']])
    timetotal = 0
    for j in range(len(timetotallist)):
        if timetotallist[j].total_seconds()<=2000:
            timetotal+=timetotallist[j].total_seconds()
    if scoreSampleFile.iloc[i]['user'] == 'drone_ar_20_010':
        timetotal = pd.Timedelta(minutes=10).total_seconds()
    elif scoreSampleFile.iloc[i]['user'] == 'drone_ar_20_011':
        timetotal = pd.Timedelta(minutes=13).total_seconds()
    elif scoreSampleFile.iloc[i]['user'] == 'drone_ar_20_015':
        timetotal = pd.Timedelta(minutes=14).total_seconds()
    l111.append(timetotal)
    l222.append(scoreSampleFile.iloc[i]['score'])
    l333.append(scoreSampleFile.iloc[i]['user'])

#plotter1 = pd.DataFrame(data={"Time":l1,"Score":l2})
#plotter1.plot.scatter(x='Time',y='Score')

#Cluster testing done here

#%matplotlib inline
#sns.set_context('poster')
#sns.set_color_codes()
#plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}


#def plot_clusters(data, algorithm, args, kwds):
#    labels = algorithm(*args, **kwds).fit_predict(data)
#    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
#    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
#    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
#    frame = plt.gca()
    #frame.axes.get_xaxis().set_visible(False)
    #frame.axes.get_yaxis().set_visible(False)
    #plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=24)

#Readying Data for clustering
X = np.array(list(zip(l111,l222)))

#plot_clusters(X, cluster.AgglomerativeClustering, (), {'n_clusters':3, 'linkage':'complete'})
#plot_clusters(X, cluster.DBSCAN, (), {'eps':120})

#Clustering
model = cluster.AgglomerativeClustering(n_clusters=3, linkage='complete')
clusterData = model.fit_predict(X)

#Finding toppers group
topGroup = []
topScore = max(l222)
for i in range(len(l222)):
    if topScore == l222[i]:
        topGroup.append(clusterData[i])
groupCounter = Counter(topGroup)

selectGroupLabel = 0
selectGroupEntries = 0
for groupLabel,values in groupCounter.items():
    if selectGroupEntries<values:
        selectGroupEntries=values
        selectGroupLabel = groupLabel


finalUserList = []
#Selecting all users from toppers group
AnalysisList = []
for i in range(len(clusterData)):
    if clusterData[i] == selectGroupLabel:
        AnalysisList.append((l333[i],l111[i]))
        finalUserList.append(l333[i])


#Analysis begins
dataUserAnalysis = data2[data2['username'].isin(finalUserList)].copy()

#Clicks
countModel = {}
averageModel = {}
graphClicks = []
for userkey,modellist in dataUserAnalysis.groupby(['username']):
    if userkey!='drone_ar_006' and userkey!='drone_ar_011':
        for model,steplist in modellist.groupby(['model_name']):
            graphClicks.append((userkey,model,len(steplist)))
            try:
                averageModel[model] += len(steplist)
                countModel[model] += 1
            except:
                averageModel[model] = len(steplist)
                countModel[model] = 1

#Final Average for clicks
#for totalmodelname in averageModel.keys():
#    print("Recommended number of times '",totalmodelname,"' should be accessed: ",int(averageModel[totalmodelname]/countModel[totalmodelname]))

clickFinalCount = []
clickModelList = list(averageModel.keys())
for totalmodelname in averageModel.keys():
    clickFinalCount.append(int(averageModel[totalmodelname]/countModel[totalmodelname]))

'''plt.figure(figsize = (20,9))
plt.bar(clickModelList,clickFinalCount)'''

#Time
avgModelTimeValue = {}
timeModel = {}
TimeCalculator = data2[data2['username'].isin(finalUserList)]
for i in TimeCalculator['username'].unique():
    UserTimeFrame = TimeCalculator[TimeCalculator['username']==i].copy()
    UserTimeFrame.reset_index()
    temp1 = [0]
    for l in range(len(UserTimeFrame['id'])-1,0,-1):
        firstime1 = pd.to_datetime(UserTimeFrame.iloc[l]['timestamp'])
        lastime1 = pd.to_datetime(UserTimeFrame.iloc[l-1]['timestamp'])
        if abs(firstime1-lastime1).total_seconds()<=2000:
            temp1.append(abs(firstime1-lastime1).total_seconds())
        else:
            temp1.append(0)
    UserTimeFrame['Duration'] = temp1
    for modelname1,modellist1 in UserTimeFrame.groupby(['model_name']):
        try:
            avgModelTimeValue[modelname1] += sum(modellist1['Duration'])
            timeModel[modelname1] += 1
        except:
            avgModelTimeValue[modelname1] = sum(modellist1['Duration'])
            timeModel[modelname1] = 1

TimeFinalCount = []
TimeModelList = list(avgModelTimeValue.keys())
for totalmodelname1 in averageModel.keys():
    TimeFinalCount.append(int(avgModelTimeValue[totalmodelname1]/timeModel[totalmodelname1]))
'''
plt.figure(figsize = (20,9))
plt.bar(TimeModelList,TimeFinalCount)'''
#avgModelTimeValue = {}
#for userkey1,modellist1 in dataUserAnalysis.groupby(['username']):
#    if userkey!='drone_ar_006' and userkey!='drone_ar_011':
#        for avgTimeKey,avgTimeValue in modellist1.groupby(['model_name']):
#            try:
#                avgModelTimeValue[avgTimeKey] += sum(avgTimeValue['model_name'])
#            except:
#                avgModelTimeValue[avgTimeKey] = sum(avgTimeValue['model_name'])
#dictsample = {'user':l3, 'score':l2}
#scoreSampleFile = pd.DataFrame(dictsample)
#scoreSampleFile.to_csv('scoreSampleFile.csv')

#l1 time l2 score l3 user
'''
l111 = []
l222 = []
l333 = []

timetotallist = []
scoreSampleFile = pd.read_csv('scoreSampleFile.csv')
for i in range(len(scoreSampleFile)):
    timetotallist = list(normalUserDiff[scoreSampleFile.iloc[i]['user']])
    timetotal = 0
    for j in range(len(timetotallist)):
        if timetotallist[j].total_seconds()<=2000:
            timetotal+=timetotallist[j].total_seconds()
    if scoreSampleFile.iloc[i]['user'] == 'drone_ar_20_010':
        timetotal = pd.Timedelta(minutes=10).total_seconds()
    elif scoreSampleFile.iloc[i]['user'] == 'drone_ar_20_011':
        timetotal = pd.Timedelta(minutes=13).total_seconds()
    elif scoreSampleFile.iloc[i]['user'] == 'drone_ar_20_015':
        timetotal = pd.Timedelta(minutes=14).total_seconds()
    l111.append(timetotal)
    l222.append(scoreSampleFile.iloc[i]['score'])
    l333.append(scoreSampleFile.iloc[i]['user'])
'''

#data2.to_csv('oneAppData.csv')
