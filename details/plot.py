import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def graphplot(l1,l2,f1):
    fig = go.Figure(
    data=[go.Bar(x=l1, y=l2)],
    layout=dict(title=dict(text=f1))
    )
    fig.write_html("./static/graph/"+f1+'.html',auto_open=False)

def Scatterplot(l1,l2,f1):
    fig = go.Figure(
    data=[go.Scatter(x=l1, y=l2)],
    layout=dict(title=dict(text=f1))
    )
    fig.write_html("./static/graph/"+f1+'.html',auto_open=False)

def pointplot(l1,l2,f1):
    fig = go.Figure(
    data=[go.Scatter(x=l1, y=l2,mode='markers')],
    layout=dict(title=dict(text=f1))
    )
    fig.write_html("./static/graph/"+f1+'.html',auto_open=False)

def plot3d(l1,l2,l3,f1):
    fig = go.Figure(data=[go.Scatter3d(x=l1, y=l2,z=l3,mode="markers",marker=dict(color=3,size=5,colorscale='Viridis',opacity=0.8,))],layout=dict(title=dict(text=f1)))
    fig.write_html("./static/graph/"+f1+'.html',auto_open=False)
