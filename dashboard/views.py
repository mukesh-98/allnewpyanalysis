from django.shortcuts import render



# Create your views here.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import math
from details import plot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots




def dashboard(request):
    try:
        data1=pd.read_csv("./static/dataframe.csv")
        if request.POST['user']=='AllUser' and request.POST['app']=='AllApp':
            appname=request.POST['app']
            SomeStartdate=pd.to_datetime(request.POST['startdate']).date()
            SomeEnddate=pd.to_datetime(request.POST['enddate']).date()
            data1=pd.read_csv("./static/dataframe.csv")
            applist=data1['app_name'].unique().tolist()
            userlist=data1['username'].unique().tolist()
            modelcount=len(data1['model_name'].unique().tolist())
            stepcount=len(data1['stepname'].unique().tolist())
            usercount=len(data1['username'].unique().tolist())
            avginc=sum(data1['Inclination'])/len(data1['Inclination'])
            plt.graphplot(userlist,applist,'userlistvsapplist')

            #Graph 2 Top 5 steps that are been clicked on very often
            step_name=[]
            step_name_count=[]
            for key,values in data1.groupby('stepname'):
                step_name.append(key)
                step_name_count.append(len(values))
                most_step=data1['stepname'].value_counts().head().index.tolist()
                most_step_count=data1['stepname'].value_counts().head().tolist()
            plt.graphplot(most_step,most_step_count,' Top 5 steps that are been clicked on very often')

            #top 5 models
            model_access_most_name = data1['model_name'].value_counts().head().index.tolist()
            model_access_most_name_count = data1['model_name'].value_counts().head().tolist()
            plt.graphplot(model_access_most_name,model_access_most_name_count,'Top 5 Models has been clicked ')

            #Average/Mean inclination of all models
            list_models = []
            list_model_Inclinations = []
            for key_model_names,modelInclinationValues in data1.groupby('model_name'):
                list_models.append(key_model_names)
                list_model_Inclinations.append(modelInclinationValues['Inclination'].mean())
            plt.pointplot(np.array(list_models),np.array(list_model_Inclinations),'Average inclination of all models')

            #Median inclination of all models
            medianlist_models = []
            medianlist_model_Inclinations = []
            for key_model_names,modelInclinationValues in data1.groupby('model_name'):
                medianlist_models.append(key_model_names)
                medianlist_model_Inclinations.append(modelInclinationValues['Inclination'].median())
            plt.Scatterplot(np.array(medianlist_models),np.array(medianlist_model_Inclinations),"Median inclination of all models")


            #Average/Mean inclination of all Steps
            list_steps = []
            list_step_Inclinations = []
            for modelInc,modelInclist in data1.groupby('model_name'):
                for stepInc,stepInclist in modelInclist.groupby('stepname'):
                    list_steps.append(modelInc+" : "+stepInc)
                    list_step_Inclinations.append(stepInclist['Inclination'].mean())
            plt.Scatterplot(np.array(list_steps),np.array(list_step_Inclinations),"Average-Mean inclination of all Steps")

            #user activity graph
            dates = [pd.to_datetime(d) for d in data1['timestamp']]
            plt.pointplot(dates,data1['username'],"user activity graph")

            #Access each day
            access_per_day = []
            day = []

            for key,value in data1.groupby('Day_name'):
                day.append(key)
                access_per_day.append(len(value))

            plt.Scatterplot(day,access_per_day,"Access each day")

            #Number of models accessed by each user
            usr=[]
            model_len=[]
            for key, value in data1.groupby('username'):
                usr.append(key)
                model=value['model_name'].unique().tolist()
                model_len.append(len(model))
            plt.Scatterplot(usr,model_len,"Number of models accessed by each user")


            data8=data1[data1['username'].isin(data1['username'].value_counts().index.tolist())]
            incx=[]
            userx=[]
            for k1,v1 in data8.groupby(data8['username']):
                userx.append(k1)
                incx.append(v1['Inclination'].mean())
            plt.pointplot(np.array(userx),np.array(incx),"User Inclination")

            #Number of month the user was online
            id_user1=[]
            usage1=[]
            for user_id1,month_usage in data1.groupby(data1['username']):
                id_user1.append(user_id1)
                usage1.append(len(month_usage['month'].value_counts()))
            plt.Scatterplot(id_user1,usage1,"Number of month the user was online")

            model_day=[]
            day_usage=[]
            for day_model,usage_day in data1.groupby(data1["model_name"]):
                model_day.append(day_model)
                day_usage.append(len(usage_day['day'].value_counts()))
            plt.Scatterplot(model_day,day_usage,"Number of month the user was online")

            #Number of Month the App was accessed
            model_month=[]
            month_usage=[]
            for month_model,usage_month in data1.groupby(data1["app_name"]):
                model_month.append(month_model)
                month_usage.append(len(usage_month['month'].value_counts()))
            plt.Scatterplot(model_month,month_usage,"Number of Month the App was accessed")

            plt.plot3d(data1['username'],data1['app_name'],data1['timestamp'],"User name Vs App name Vs TimeStamp")
            plt.plot3d(data1['username'],data1['app_name'],data1['Inclination'],"User name Vs App name Vs Inclination")
            plt.plot3d(data1['app_name'],data1['model_name'],data1['stepname'],"App name Vs Model name Vs Step name")
            plt.plot3d(data1['app_name'],data1['timestamp'],data1['Inclination'],"App name Vs TimeStamp Vs Inclination")



            return render(request,'dashboard.html',{'app':appname,'name':"All User",'counts':usercount,'model':modelcount,'step':stepcount,'avginc':str(avginc)[:6],'alluser':True,'allapp':True})

        elif request.POST['user']=='AllUser':
            data1=pd.read_csv("./static/dataframe.csv")
            SomeAppname=request.POST['app']
            SomeUsername=request.POST['user']
            SomeStartdate=request.POST['startdate']
            SomeEnddate=request.POST['enddate']
            SelectedDataUser = data1 #username slice
            SelectedDataApp = SelectedDataUser[SelectedDataUser['app_name'] == SomeAppname] #App slice
            DateMask = (SelectedDataApp['Date']>=SomeStartdate) & (SelectedDataApp['Date']<=SomeEnddate) #Date mask for start and end date
            SelectedDataFinalapp = SelectedDataApp.loc[DateMask] #data used in data analytics
            modelcount=len(SelectedDataFinalapp['model_name'].unique().tolist())
            stepcount=len(SelectedDataFinalapp['stepname'].unique().tolist())
            usercount=len(SelectedDataFinalapp['username'].unique().tolist())
            avginc=sum(SelectedDataFinalapp['Inclination'])/len(SelectedDataFinalapp['Inclination'])
            #Access Date of User
            access_date=[]
            access_date_counts=[]
            access_date_inc=[]
            access_date_counts=SelectedDataFinalapp['Date'].value_counts().tolist()
            access_date=SelectedDataFinalapp['Date'].value_counts().index.tolist()
            access_date_inc=SelectedDataFinalapp['Inclination'].tolist()
            plt.pointplot(access_date,access_date_counts,"Access Date of User")

            #Inclination of User of each Date
            plt.Scatterplot(access_date,access_date_inc,"Inclination of User of each Date")


            #Access Model of User
            access_model=[]
            access_model_counts=[]
            access_model_counts=SelectedDataFinalapp['model_name'].value_counts().tolist()
            access_model=SelectedDataFinalapp['model_name'].value_counts().index.tolist()
            plt.pointplot(access_model,access_model_counts,"Access Model of User")


            #Access Step of User
            access_step=[]
            access_step_counts=[]
            for key,values in SelectedDataFinalapp.groupby(SelectedDataFinalapp['model_name']):
                access_step_counts=SelectedDataFinalapp['stepname'].value_counts().tolist()
                access_step=SelectedDataFinalapp['stepname'].value_counts().index.tolist()
            plt.Scatterplot(access_step,access_step_counts,"Access Step of User")
                #-----------------------------------------------------------------------------------------------------------


            list_models = []
            list_model_Inclinations = []
            for key_model_names,modelInclinationValues in SelectedDataFinalapp.groupby('model_name'):
                list_models.append(key_model_names)
                list_model_Inclinations.append(modelInclinationValues['Inclination'].mean())
            plt.pointplot(np.array(list_models),np.array(list_model_Inclinations),'Average inclination of all models of User')

            #Median inclination of all models
            medianlist_models = []
            medianlist_model_Inclinations = []
            for key_model_names,modelInclinationValues in SelectedDataFinalapp.groupby('model_name'):
                medianlist_models.append(key_model_names)
                medianlist_model_Inclinations.append(modelInclinationValues['Inclination'].median())
            plt.Scatterplot(np.array(medianlist_models),np.array(medianlist_model_Inclinations),"Median inclination of all models of User")

            #Average/Mean inclination of all Steps
            list_steps = []
            list_step_Inclinations = []
            for modelInc,modelInclist in SelectedDataFinalapp.groupby('model_name'):
                for stepInc,stepInclist in modelInclist.groupby('stepname'):
                    list_steps.append(modelInc+" : "+stepInc)
                    list_step_Inclinations.append(stepInclist['Inclination'].mean())
            plt.Scatterplot(np.array(list_steps),np.array(list_step_Inclinations),"Average-Mean inclination of all Steps of User")

            #user activity graph
            dates = [pd.to_datetime(d) for d in SelectedDataFinalapp['timestamp']]
            plt.pointplot(dates,SelectedDataFinalapp['username'],"user activity graph of user")

            #Access each day
            access_per_day = []
            day = []

            for key,value in SelectedDataFinalapp.groupby('Day_name'):
                day.append(key)
                access_per_day.append(len(value))

            plt.Scatterplot(day,access_per_day,"Access each day  of user")

            #Number of models accessed by each user
            usr=[]
            model_len=[]
            for key, value in SelectedDataFinalapp.groupby('username'):
                usr.append(key)
                model=value['model_name'].unique().tolist()
                model_len.append(len(model))
            plt.Scatterplot(usr,model_len,"Number of models accessed By user")


            data8=SelectedDataFinalapp[SelectedDataFinalapp['username'].isin(SelectedDataFinalapp['username'].value_counts().index.tolist())]
            incx=[]
            userx=[]
            for k1,v1 in data8.groupby(data8['username']):
                userx.append(k1)
                incx.append(v1['Inclination'].mean())
            plt.pointplot(np.array(userx),np.array(incx),"User-Inclination")

            #Number of month the user was online
            id_user1=[]
            usage1=[]
            for user_id1,month_usage in SelectedDataFinalapp.groupby(SelectedDataFinalapp['username']):
                id_user1.append(user_id1)
                usage1.append(len(month_usage['month'].value_counts()))
            plt.Scatterplot(id_user1,usage1,"Number of month the User was online")

            model_day=[]
            day_usage=[]
            for day_model,usage_day in SelectedDataFinalapp.groupby(SelectedDataFinalapp["model_name"]):
                model_day.append(day_model)
                day_usage.append(len(usage_day['day'].value_counts()))
            plt.Scatterplot(model_day,day_usage,"Number of Day the User was online")

            #Number of Month the App was accessed
            model_month=[]
            month_usage=[]
            for month_model,usage_month in SelectedDataFinalapp.groupby(SelectedDataFinalapp["app_name"]):
                model_month.append(month_model)
                month_usage.append(len(usage_month['month'].value_counts()))
            plt.Scatterplot(model_month,month_usage,"Number of Month the App was Accessed")

            plt.plot3d(SelectedDataFinalapp['username'],SelectedDataFinalapp['model_name'],SelectedDataFinalapp['timestamp'],"User name Vs Model_name Vs TimeStamp")
            plt.plot3d(SelectedDataFinalapp['username'],SelectedDataFinalapp['model_name'],SelectedDataFinalapp['Inclination'],"User name Vs Model name Vs Inclination")
            plt.plot3d(SelectedDataFinalapp['username'],SelectedDataFinalapp['model_name'],SelectedDataFinalapp['stepname'],"User name Vs Model name Vs Step name")
            plt.plot3d(SelectedDataFinalapp['model_name'],SelectedDataFinalapp['timestamp'],SelectedDataFinalapp['Inclination'],"Model name Vs TimeStamp Vs Inclination")
            return render(request,'dashboard.html',{'app':SomeAppname,'name':"All User",'counts':usercount,'model':modelcount,'step':stepcount,'avginc':str(avginc)[:6],'alluser':True})

        elif request.POST['user'] !='AllUser' and request.POST['app']=='AllApp' or pd.to_datetime(request.POST['enddate']) <  pd.to_datetime(min(data1['Date'])) :
            return render(request,'dashboard.html',{'app':request.POST['app'],'name':request.POST['user'],'counts':0,'model':0,'step':0,'avginc':0,'alluser':False,'allapp':True})

        elif  pd.to_datetime(request.POST['enddate']) <  pd.to_datetime(min(data1['Date'])) :
            return render(request,'dashboard.html',{'app':request.POST['app'],'name':request.POST['user'],'counts':0,'model':0,'step':0,'avginc':0,'alluser':False,'allapp':True})

        else:
            data1=pd.read_csv("./static/dataframe.csv")
            SomeAppname=request.POST['app']
            SomeUsername=request.POST['user']
            SomeStartdate=request.POST['startdate']
            SomeEnddate=request.POST['enddate']


            SelectedDataUser = data1[data1['username'] == SomeUsername] #username slice
            SelectedDataApp = SelectedDataUser[SelectedDataUser['app_name'] == SomeAppname] #App slice
            DateMask = (SelectedDataApp['Date']>=SomeStartdate) & (SelectedDataApp['Date']<=SomeEnddate) #Date mask for start and end date
            SelectedDataFinal = SelectedDataApp.loc[DateMask] #data used in data analytics

            modelcount=len(SelectedDataFinal['model_name'].unique().tolist())
            stepcount=len(SelectedDataFinal['stepname'].unique().tolist())
            usercount=len(SelectedDataFinal['username'].unique().tolist())
            avginc=sum(SelectedDataFinal['Inclination'])/len(SelectedDataFinal['Inclination'])

            #Access Date of User
            access_date=[]
            access_date_counts=[]
            access_date_inc=[]
            access_date_counts=SelectedDataFinal['Date'].value_counts().tolist()
            access_date=SelectedDataFinal['Date'].value_counts().index.tolist()
            access_date_inc=SelectedDataFinal['Inclination'].tolist()
            plt.pointplot(access_date,access_date_counts,"Access Date of User")

            #Inclination of User of each Date
            plt.Scatterplot(access_date,access_date_inc,"Inclination of User of each Date")


            #Access Model of User
            access_model=[]
            access_model_counts=[]
            access_model_counts=SelectedDataFinal['model_name'].value_counts().tolist()
            access_model=SelectedDataFinal['model_name'].value_counts().index.tolist()
            plt.pointplot(access_model,access_model_counts,"Access Model of User")


            #Access Step of User
            access_step=[]
            access_step_counts=[]
            for key,values in SelectedDataFinal.groupby(SelectedDataFinal['model_name']):
                access_step_counts=SelectedDataFinal['stepname'].value_counts().tolist()
                access_step=SelectedDataFinal['stepname'].value_counts().index.tolist()
            plt.Scatterplot(access_step,access_step_counts,"Access Step of User")
            #-----------------------------------------------------------------------------------------------------------


            list_models = []
            list_model_Inclinations = []
            for key_model_names,modelInclinationValues in SelectedDataFinal.groupby('model_name'):
                list_models.append(key_model_names)
                list_model_Inclinations.append(modelInclinationValues['Inclination'].mean())
            plt.pointplot(np.array(list_models),np.array(list_model_Inclinations),'Average inclination of all models of User')

            #Median inclination of all models
            medianlist_models = []
            medianlist_model_Inclinations = []
            for key_model_names,modelInclinationValues in SelectedDataFinal.groupby('model_name'):
                medianlist_models.append(key_model_names)
                medianlist_model_Inclinations.append(modelInclinationValues['Inclination'].median())
            plt.Scatterplot(np.array(medianlist_models),np.array(medianlist_model_Inclinations),"Median inclination of all models of User")


            #Average/Mean inclination of all Steps
            list_steps = []
            list_step_Inclinations = []
            for modelInc,modelInclist in SelectedDataFinal.groupby('model_name'):
                for stepInc,stepInclist in modelInclist.groupby('stepname'):
                    list_steps.append(modelInc+" : "+stepInc)
                    list_step_Inclinations.append(stepInclist['Inclination'].mean())
            plt.Scatterplot(np.array(list_steps),np.array(list_step_Inclinations),"Average-Mean inclination of all Steps of User")

            #user activity graph
            dates = [pd.to_datetime(d) for d in SelectedDataFinal['timestamp']]
            plt.pointplot(dates,SelectedDataFinal['username'],"user activity graph of user")

            #Access each day
            access_per_day = []
            day = []

            for key,value in SelectedDataFinal.groupby('Day_name'):
                day.append(key)
                access_per_day.append(len(value))

            plt.Scatterplot(day,access_per_day,"Access each day  of user")

            #Number of models accessed by each user
            usr=[]
            model_len=[]
            for key, value in SelectedDataFinal.groupby('username'):
                usr.append(key)
                model=value['model_name'].unique().tolist()
                model_len.append(len(model))
            plt.Scatterplot(usr,model_len,"Number of models accessed By user")


            data8=SelectedDataFinal[SelectedDataFinal['username'].isin(SelectedDataFinal['username'].value_counts().index.tolist())]
            incx=[]
            userx=[]
            for k1,v1 in data8.groupby(data8['username']):
                userx.append(k1)
                incx.append(v1['Inclination'].mean())
            plt.pointplot(np.array(userx),np.array(incx),"User-Inclination")

            #Number of month the user was online
            id_user1=[]
            usage1=[]
            for user_id1,month_usage in SelectedDataFinal.groupby(SelectedDataFinal['username']):
                id_user1.append(user_id1)
                usage1.append(len(month_usage['month'].value_counts()))
            plt.Scatterplot(id_user1,usage1,"Number of month the User was online")

            model_day=[]
            day_usage=[]
            for day_model,usage_day in SelectedDataFinal.groupby(SelectedDataFinal["model_name"]):
                model_day.append(day_model)
                day_usage.append(len(usage_day['day'].value_counts()))
            plt.Scatterplot(model_day,day_usage,"Number of Day the User was online")

            #Number of Month the App was accessed
            model_month=[]
            month_usage=[]
            for month_model,usage_month in SelectedDataFinal.groupby(SelectedDataFinal["app_name"]):
                model_month.append(month_model)
                month_usage.append(len(usage_month['month'].value_counts()))
            plt.Scatterplot(model_month,month_usage,"Number of Month the App was Accessed")

            plt.plot3d(SelectedDataFinal['stepname'],SelectedDataFinal['model_name'],SelectedDataFinal['timestamp'],"Step name Vs Model_name Vs TimeStamp")
            plt.plot3d(SelectedDataFinal['stepname'],SelectedDataFinal['model_name'],SelectedDataFinal['Inclination'],"Step name Vs Model name Vs Inclination")
            plt.plot3d(SelectedDataFinal['year'],SelectedDataFinal['model_name'],SelectedDataFinal['stepname'],"Year Vs Model name Vs Step name")
            plt.plot3d(SelectedDataFinal['model_name'],SelectedDataFinal['timestamp'],SelectedDataFinal['Inclination'],"Model name Vs TimeStamp Vs Inclination")

            return render(request,'dashboard.html',{'app':SomeAppname,'name':SomeUsername,'counts':usercount,'model':modelcount,'step':stepcount,'avginc':str(avginc)[:6],'alluser':False})
    except:
        return render(request,'dashboard.html')
