#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff


# In[2]:


data = pd.read_csv('netflix_titles.csv')
data.head(3)


# In[3]:


data.info() #Explore the data


# In[4]:


#Checking for null values
data.isnull().sum()


# In[5]:


#number of unique values in the dataset
data.nunique()


# In[7]:


#Data cleaning 
#Dropping values
data = data.dropna(how='any',subset=['cast','director'])


# In[8]:


#Replace NULL values with "missing"
data['country'].fillna("Missing",inplace=True)
data['date_added'].fillna("Missing",inplace=True)
data['rating'].fillna("Missing",inplace=True)


# In[9]:


#year format
data['date_added'] = pd.to_datetime(data['date_added'])
data['year_added'] = data['date_added'].dt.year
data["month_added"] = data['date_added'].dt.month


# In[10]:


#Seasons from Duration
df['season_count'] = data.apply(lambda x : x['duration'].split(" ")[0] if "Season" in x['duration'] else "", axis = 1)
df['duration'] = data.apply(lambda x : x['duration'].split(" ")[0] if "Season" not in x['duration'] else "", axis = 1)


# In[11]:


data = data.rename(columns={"listed_in":"genre"})
data['genre'] = data['genre'].apply(lambda x: x.split(",")[0])
data.head(5)


# In[12]:


data.describe(include = "O")


# In[13]:


#Visualization
#Correlation between the feature show with the help of visualization
corrs = data.corr()
fig_heatmap = ff.create_annotated_heatmap(
    z=corrs.values,
    x=list(corrs.columns),
    y=list(corrs.index),
    annotation_text = corrs.round(2).values,
    showscale=True)
fig_heatmap.update_layout(title= 'Corelation of whole data',
                         plot_bgcolor='#2d3035',paper_bgcolor='teal',
                         title_font=dict(size=25,color='#17202A',family="Muli,comfortaa"),
                         font=dict(color='#050505'))


# In[14]:


#Movies v/s TV Shows
fig_donut= px.pie(data,names="type",height = 300,width=600,hole=0.7,
title = "Most watched on Netflix",color_discrete_sequence=['#b20710','#221f1f'])
fig_donut.update_traces(hovertemplate=None, textposition='outside', textinfo='percent+label',rotation=90)
fig_donut.update_layout(margin=dict(t=60,b=30,l=0,r=0), showlegend=False,
                       plot_bgcolor='#333', paper_bgcolor='#333',

title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),

font=dict(size=17, color='#8a8d93'),

hoverlabel=dict(bgcolor="#444", font_size=13,

font_family="Lato, sans-serif"))


# In[17]:


#What the audience prefer to watch?
data_rating = pd.DataFrame(data['rating'].value_counts()).reset_index().rename(columns={'index':'rating','rating':
                                                                                   'count'})
fig_bar = px.bar(data_rating, y='rating',x='count',title='Distribution of Rating',color_discrete_sequence=['#b20710'],text='count')
fig_bar.update_xaxes(showgrid=False)
fig_bar.update_yaxes(showgrid=False,categoryorder='total ascending',ticksuffix = '',showline=False)
fig_bar.update_traces(hovertemplate=None, marker=dict(line=dict(width=0)))
fig_bar.update_layout(margin=dict(t=80, b=0, l=70, r=40),
hovermode="y unified",
xaxis_title=' ', yaxis_title=" ", height=400,
plot_bgcolor='#333', paper_bgcolor='#333',
title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
font=dict(color='#8a8d93'),
legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
hoverlabel=dict(bgcolor="black", font_size=13, font_family="Lato, sans-serif")) 


# In[18]:


dff = data.copy()
# making 2 df one for tv show and another for movie with rating 
df_tv_show = dff[dff['type']=='TV Show'][['rating', 'type']].rename(columns={'type':'tv_show'})
df_movie = dff[dff['type']=='Movie'][['rating', 'type']].rename(columns={'type':'movie'})
df_tv_show = pd.DataFrame(df_tv_show.rating.value_counts()).reset_index().rename(columns={'index':'tv_show'})
df_tv_show['rating_final'] = df_tv_show['rating'] 
# making rating column value negative
df_tv_show['rating'] *= -1
df_movie = pd.DataFrame(df_movie.rating.value_counts()).reset_index().rename(columns={'index':'movie'})


# In[21]:


fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)
# bar plot for tv shows
fig.append_trace(go.Bar(x=df_tv_show.rating, y=df_tv_show.tv_show, orientation='h', showlegend=True, 
                        text=df_tv_show.rating_final, name='TV Show', marker_color='#221f1f'), 1, 1)
# bar plot for movies
fig.append_trace(go.Bar(x=df_movie.rating, y=df_movie.movie, orientation='h', showlegend=True, text=df_movie.rating,
                        name='Movie', marker_color='#b20710'), 1, 2)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False, categoryorder='total ascending', ticksuffix=' ', showline=False)
fig.update_traces(hovertemplate=None, marker=dict(line=dict(width=0)))
fig.update_layout(title='Which has the highest rating TV shows or Movies?',
                  margin=dict(t=80, b=0, l=70, r=40),
                  hovermode="y unified", 
                  xaxis_title=' ', yaxis_title=" ",
                  plot_bgcolor='#333', paper_bgcolor='#333',
                  title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
                  font=dict(color='#8a8d93'),
                  legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
                  hoverlabel=dict(bgcolor="black", font_size=13, font_family="Lato, sans-serif"))
fig.add_annotation(dict(x=0.81, y=0.6, ax=0, ay=0,
                    xref = "paper", yref = "paper",
                    text= "97% people prefer Movies over TV Shows on Netflix.Large number of people watch TV-MA rating   Movies which are for mature audience."
                  ))
fig.add_annotation(dict(x=0.2, y=0.2, ax=0, ay=0,
                    xref = "paper", yref = "paper",
                    text= "3% people prefer TV Shows on Netflix. There is no inappropriate content for ages 17 and under in TV Shows."
                  ))


# In[24]:


data_month = pd.DataFrame(data.month_added.value_counts()).reset_index().rename(columns={'index':'month','month_added':'count'})
# converting month number to month name
data_month['month_final'] = data_month['month'].replace({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'June', 7:'July', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})
data_month[:2]


# In[26]:


fig_month = px.funnel(data_month, x='count', y='month_final', title='Best month for releasing Content',
                      height=350, width=600, color_discrete_sequence=['#b20710'])
fig_month.update_xaxes(showgrid=False, ticksuffix=' ', showline=True)
fig_month.update_traces(hovertemplate=None, marker=dict(line=dict(width=0)))
fig_month.update_layout(margin=dict(t=60, b=20, l=70, r=40),
                        xaxis_title=' ', yaxis_title=" ",
                        plot_bgcolor='#333', paper_bgcolor='#333',
                        title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
                        font=dict(color='#8a8d93'),
                        hoverlabel=dict(bgcolor="black", font_size=13, font_family="Lato, sans-serif"))


# In[28]:


data_genre = pd.DataFrame(data.genre.value_counts()).reset_index().rename(columns={'index':'genre', 'genre':'count'})
fig_tree = px.treemap(data_genre, path=[px.Constant("Distribution of Geners"), 'count','genre'])
fig_tree.update_layout(title='Highest watched Geners on Netflix',
                  margin=dict(t=50, b=0, l=70, r=40),
                  plot_bgcolor='#333', paper_bgcolor='#333',
                  title_font=dict(size=25, color='#fff', family="Lato, sans-serif"),
                  font=dict(color='#8a8d93'),
                  hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))


# In[29]:


d2 = data[data["type"] == "Movie"]
d2[:2]


# In[30]:


col ='year_added'

vc2 = d2[col].value_counts().reset_index().rename(columns = {col : "count", "index" : col})

vc2['percent'] = vc2['count'].apply(lambda x : 100*x/sum(vc2['count']))

vc2 = vc2.sort_values(col)

vc2[:3]


# In[31]:


fig1 = go.Figure(go.Waterfall(
    name = "Movie", orientation = "v", 
    x = vc2['year_added'].values,
    textposition = "auto",
    text = ["1", "2", "1", "13", "3", "6", "14", "48", "204", "743", "1121", "1366", "1228", "84"],
    y = [1, 2, -1, 13, -3, 6, 14, 48, 204, 743, 1121, 1366, -1228, -84],
    connector = {"line":{"color":"#b20710"}},
    increasing = {"marker":{"color":"#b20710"}},
    decreasing = {"marker":{"color":"orange"}},
))
fig1.show()


# In[32]:


d1 = data[data["type"] == "TV Show"]
d2 = data[data["type"] == "Movie"]
col = "year_added"
vc1 = d1[col].value_counts().reset_index().rename(columns = {col : "count", "index" : col})
vc1['percent'] = vc1['count'].apply(lambda x : 100*x/sum(vc1['count']))
vc1 = vc1.sort_values(col)
vc2 = d2[col].value_counts().reset_index().rename(columns = {col : "count", "index" : col})
vc2['percent'] = vc2['count'].apply(lambda x : 100*x/sum(vc2['count']))
vc2 = vc2.sort_values(col)
trace1 = go.Scatter(x=vc1[col], y=vc1["count"], name="TV Shows", marker=dict(color="orange"), )
trace2 = go.Scatter(x=vc2[col], y=vc2["count"], name="Movies", marker=dict(color="#b20710"))
data = [trace1, trace2]
fig_line = go.Figure(data)
fig_line.update_traces(hovertemplate=None)
fig_line.update_xaxes(showgrid=False)
fig_line.update_yaxes(showgrid=False)
large_title_format = 'Tv Show and Movies impact over the Year'
small_title_format = "Due to Covid updatation of content is slowed." 
fig_line.update_layout(title=large_title_format + " " + small_title_format, 
    height=400, margin=dict(t=130, b=0, l=70, r=40), 
    hovermode="x unified", xaxis_title=' ', 
    yaxis_title=" ", plot_bgcolor='#333', paper_bgcolor='#333', 
    title_font=dict(size=25, color='#8a8d93',
    family="Lato, sans-serif"),
    font=dict(color='#8a8d93'),
    legend=dict(orientation="h",
    yanchor="bottom",
    y=1,
    xanchor="center",
    x=0.5)) 
fig_line.add_annotation(dict
    (x=0.8, 
    y=0.3,
    ax=0, 
    ay=0,
    xref = "paper",
    yref = "paper",
    text= "Highest number of Tv Shows were released in 2019 followed by 2017." )) 
fig_line.add_annotation(dict
    (x=0.9, 
    y=1,
    ax=0,
    ay=0,
    xref = "paper",
    yref = "paper",
    text= "Highest number of Movies were relased in 2019 followed by 2020" )) 
fig_line.show()


# In[ ]:




