import plotly
import plotly.graph_objs as go
import pandas as pd

def Scatter_Plot2(df,colour,x_axis,y_axis,mode,display,fill,filename):  
    
    
    cat_list = df[colour].unique()
    cat_list = sorted(cat_list, reverse=True)
    
    data=[]
    
    for item in cat_list:
        x=df.loc[df[colour] == item][x_axis]
        y=df.loc[df[colour] == item][y_axis]
        
        
        try:
        	friend_colour = '#'+str(friend_df.loc[friend_df['name'] == item,'colour'].values[0])
        except:
        	friend_colour = '#646464'
        
        trace = go.Scatter(
            x=x,
            y=y,
            name=item,
            mode=mode,
            fill=fill,
            fillcolor = friend_colour,
            line=dict(color = friend_colour)
           
            )
        data.append(trace) 
    
    layout = go.Layout( 
        xaxis = {'title': x_axis},
        yaxis = {'title': y_axis},
        legend = {'x': 100}
      
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=filename+'_plot.html',auto_open=False)
    return

def Bar_Plot(df,colour,x_axis,y_axis,mode,display,fill,filename):  
    
    
    df = df.sort_values([y_axis], ascending=False)
    df['colour'] = '#' + df['colour'].astype(str)
    x=df[colour]
    y=df[y_axis]

    colour = df['colour']
    
    
    
    data=[]
    
    
    trace = go.Bar(
        x=x,
        y=y,
        #name=item,
        #mode=mode,
        #fill=fill,
        marker=dict(color=colour),
        #fillcolor = '#646464',
        #line=dict(color = friend_colour)
       
        )
    data.append(trace) 
    
    layout = go.Layout( 
        xaxis = {'title': x_axis},
        yaxis = {'title': y_axis},
        legend = {'x': 100}
      
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=filename+'_plot.html',auto_open=False)
    return

friend_df = pd.read_csv('friend_colour_new.csv',index_col=False)

#line graph of segments over time:
df = pd.read_csv('segmentcountovertime.csv')
Scatter_Plot2(df,'name','date','count','lines','count','','segments_over_time')

#stacked graph of segments over time:
df_cumsum = df.groupby(by=['date','name']).max().groupby(level=[0]).cumsum()['count']
df_cumsum = df_cumsum.unstack().fillna(0).stack()
df_cumsum = df_cumsum.reset_index()
df_cumsum.rename(columns={0: 'count'}, inplace=True)
Scatter_Plot2(df_cumsum,'name','date','count','lines','count','tozeroy','stacked')

#bar graph of current segment count snapshot:
df_snapshot = pd.read_csv('segmentcount.csv')
Bar_Plot(df_snapshot,'name','date','count','lines','count','tozeroy','segment_count_snapshot')