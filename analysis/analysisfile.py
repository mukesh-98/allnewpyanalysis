import statistics as stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import re
from faker import Faker
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from details import views as details

data = pd.read_csv("analysis/Tracking-2020-02-22.csv")

data=details.work(data)

timeDiff=[]
for i in range(len(data['id'])-1,0,-1):
    firstime = pd.to_datetime(data.iloc[i]['timestamp'])
    lastime = pd.to_datetime(data.iloc[i-1]['timestamp'])
    timeDiff.append(abs(firstime-lastime))

#function to convert seconds back into time delta
def convert_seconds(second):
    return pd.Timedelta(seconds = second)

#creating a dataframe with steps and time taken as column (by ideal user) and plotting Ideal curve
steps = data['stepname'].sort_index(ascending=False)
steps.pop(713)
plotter = pd.DataFrame(data={"steps":steps,"TimeDiff":[x.total_seconds() for x in timeDiff]})
#plotter.plot.scatter(x='steps',y='TimeDiff')

#extracting and refining 10 normal users
data2 = pd.read_csv("analysis/Tracking-2020-02-22.csv")
data2=data2.drop(["lon","lat"],axis=1)
data2=data2.dropna()

#Extracting enteries only for "drone fundamentals" app
for app,data2 in data2.groupby(['app_name']):
    if app=="Drone_Fundamentals":
        break
#Removing "junaid"(ideal user) entries
data2=data2.drop(data2.index[data2['username']=="junaid"].tolist())
normalUsers = data2['username'].unique().tolist() #list of all the unique users excluding ideal user

#removes all the test users (may require multiple passes )
for i in normalUsers:
    if not re.search("^drone",i):
        normalUsers.pop(normalUsers.index(i))

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

#importing data of user who have taken test
data3 = pd.read_csv("analysis/DBIT_-_Drone_Design_and_Aviation_-_2020_-_Quiz_Responses.csv")
data3 = data3.drop([2])
marks = data3.loc[[0,1,7,14,11,4,10,18,17]]
tempo = {"Score":marks['Score'],"time":[],"Users":marks['username']}
for user in marks['username']:
    temp = normalUserDiff[user]
    alltime= pd.Timedelta(0)
    for i in temp:
        alltime += i
    tempo["time"].append(alltime.total_seconds())
    alltime=pd.Timedelta(0)

tempo['time'][4] = pd.Timedelta(minutes=10).total_seconds()
tempo['time'][5] = pd.Timedelta(minutes=13).total_seconds()
tempo['time'][7] = pd.Timedelta(minutes=14).total_seconds()

main = pd.DataFrame(data=tempo['Score'])
main1 = pd.DataFrame(data=tempo['time'])
regr = LinearRegression()
regr.fit(main1,main)
y_pred = regr.predict(main1)



'''
RegDict = {'time':tempo['time'],'score':list(tempo['Score']),'user':tempo['Users']}
RegUserList = list(RegDict['user'])
DataRegSample = data2[data2['username'].isin(RegUserList)].copy()
DataRegSample['Inclination'] = np.degrees(np.arccos(DataRegSample['accelerometer_z']/np.sqrt(pow(DataRegSample['accelerometer_x'],2)+pow(DataRegSample['accelerometer_y'],2)+pow(DataRegSample['accelerometer_z'],2))))

A = []
B = []
C = []
for userKey,userVal in DataRegSample.groupby(['username']):
    B.append(userVal['Inclination'].std())
    A.append(userKey)

otherUserList = list(RegDict['user'])
OtherUserTime = list(RegDict['time'])
OtherUserScore = list(RegDict['score'])
OtherUserSD = [0.0]*len(otherUserList)

for i in range(len(otherUserList)):
    OtherUserSD[i] = B[A.index(otherUserList[i])]

FinalRegDict = {'Time':OtherUserTime,'St':OtherUserSD,'Score':OtherUserScore}
RegDataFrame = pd.DataFrame(FinalRegDict)


#min_max_scaler = preprocessing.MinMaxScaler()
min_max_scaler = preprocessing.MaxAbsScaler()
X = RegDataFrame[['Time','St']].copy()
X[['Time','St']] = min_max_scaler.fit_transform(X[['Time','St']])
#X['St'] = min_max_scaler.fit_transform(X['St'])
Y = RegDataFrame['Score'].copy()
regr2 = LinearRegression()
regr2.fit(X,Y)
y_pred2 = regr2.predict(X)


testdata = pd.DataFrame(data={'time':[823]})
test_pred = regr.predict(testdata)'''
