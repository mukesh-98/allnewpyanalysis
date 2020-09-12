from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import math
from details import plot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from analysis import analysisfile as an
from collections import Counter
import seaborn as sns
import datetime
import re
from sklearn.linear_model import LinearRegression
import sklearn.cluster as cluster


def analysis(request):
    try:
        x=an.main1
        y=request.POST['Time']
        if y=='':
            return render(request,'analysis.html',{'y':0})
        else:
            y= pd.DataFrame(data={'time':[request.POST['Time']]})
            marks=an.regr.predict(y)
            if marks>max(an.tempo['Score']):
                marks=[['Entered time is greater then expected time']]
        if request.method== 'POST':
            file2 = request.FILES['file_2']
            if file2 != '':
                fs2=FileSystemStorage()
                name2=fs2.save(file2.name,file2)
                url2=fs2.url(name2)


            file3 = request.FILES['file_3']
            if file3 != '':
                fs3=FileSystemStorage()
                name3=fs3.save(file3.name,file3)
                url3=fs3.url(name3)




        try:
            data2 = pd.read_csv("."+url2)
            x=pd.read_csv("./analysis/oneAppData.csv")
            scoreSampleFile =pd.read_csv("."+url3)
            y=pd.read_csv("./analysis/scoreSampleFile.csv")

            data2=data2.drop(["accelerometer_x","accelerometer_x","accelerometer_y","accelerometer_z","lon","lat"],axis=1)
            data2=data2.dropna()

            data2=data2.drop(data2.index[data2['username']=="junaid"].tolist())
            normalUsers = data2['username'].unique().tolist()
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

            clickFinalCount = []
            clickModelList = list(averageModel.keys())
            for totalmodelname in averageModel.keys():
                clickFinalCount.append(int(averageModel[totalmodelname]/countModel[totalmodelname]))


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
            plt.graphplot(clickModelList,clickFinalCount,"Clicks Clustering")
            plt.graphplot(TimeModelList,TimeFinalCount,"Time Clustering")
            return render(request,'analysis.html',{'y':int(marks[0][0])})
        except KeyError:
            return render(request,'analysis.html',{'y':"You Selected Wrong File"})
    except :
        return render(request,'dashboard.html')
