import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import statistics


postal = {'WA': 'WASHINGTON', 'VA': 'VIRGINIA', 'DE': 'DELAWARE', 'DC': 'DISTRICT OF COLUMBIA', 'WI': 'WISCONSIN', 'WV': 'WEST VIRGINIA', 'HI': 'HAWAII', 'FL': 'FLORIDA', 'FM': 'FEDERATED STATES OF MICRONESIA', 'WY': 'WYOMING', 'NH': 'NEW HAMPSHIRE', 'NJ': 'NEW JERSEY', 'NM': 'NEW MEXICO', 'TX': 'TEXAS', 'LA': 'LOUISIANA', 'NC': 'NORTH CAROLINA', 'ND': 'NORTH DAKOTA', 'NE': 'NEBRASKA', 'TN': 'TENNESSEE', 'NY': 'NEW YORK', 'PA': 'PENNSYLVANIA', 'CA': 'CALIFORNIA', 'NV': 'NEVADA', 'PW': 'PALAU', 'Gu': 'GUAM GU', 'CO': 'COLORADO', 'Vi': 'VIRGIN ISLANDS', 'AK': 'ALASKA', 'AL': 'ALABAMA', 'AS': 'AMERICAN SAMOA', 'AR': 'ARKANSAS', 'VT': 'VERMONT', 'IL': 'ILLINOIS', 'GA': 'GEORGIA', 'IN': 'INDIANA', 'IA': 'IOWA', 'OK': 'OKLAHOMA', 'AZ': 'ARIZONA', 'ID': 'IDAHO', 'CT': 'CONNECTICUT', 'ME': 'MAINE', 'MD': 'MARYLAND', 'MA': 'MASSACHUSETTS', 'OH': 'OHIO', 'UT': 'UTAH', 'MO': 'MISSOURI', 'MN': 'MINNESOTA', 'MI': 'MICHIGAN', 'MH': 'MARSHALL ISLANDS', 'RI': 'RHODE ISLAND', 'KS': 'KANSAS', 'MT': 'MONTANA', 'MP': 'NORTHERN MARIANA ISLANDS', 'MS': 'MISSISSIPPI', 'PR': 'PUERTO RICO', 'SC': 'SOUTH CAROLINA', 'KY': 'KENTUCKY', 'OR': 'OREGON', 'SD': 'SOUTH DAKOTA'}
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('after removing duplicates.csv')
server =app.server
controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("State",color='light'),
                dcc.Dropdown(
                    id="state",
                    options=[{'label': postal[i], 'value': i} for i in df['State'].unique()],
                    value=[],
                    multi=True
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Medicare Part",color="light"),
                dcc.Dropdown(
                    id="Medicare part",
                    options=[{'label':i , 'value': i} for i in df['Medicare Part'].unique()],
                    value=[],
                    multi=True
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Appeal Category",color="light"),
                dcc.Dropdown(
                        id='Appeal category',
                        options=[{'label':i , 'value': i} for i in df['Appeal Category'].unique()],
                        value=[],
                        multi=True
                ),
            ]
        ),
        dbc.FormGroup(
            [
            dbc.Label("Major Procedure Category",color="light"),
            dcc.Dropdown(
                    id='Procedure code',
                    options=[{'label':i , 'value': i} for i in df['Procedure Code'].unique()],
                    value=[],
                    multi=True
                ),
            ]
        ),
        dbc.FormGroup(
            [
            dbc.Button(id='submit_button',
                        n_clicks=0,color="light", className="mr-1",
                        children='Apply',
                )
            ]
        ),
        dbc.FormGroup(
            [
            dbc.Button(
                       id='clear-button',
                       n_clicks=0,color="light", className="mr-1",
                       children='Clear',
              )
            ]
        )
    ],
    body=True,
    color='dark',
)

smallcard1=dbc.Card(
                  [
                  dbc.CardHeader(html.H4("Avg.Processing Days", style={"font-family": "Arial, Helvetica, sans-serif","color":'white'},className="card-title")),
                  dbc.CardBody(
                     [
                        html.H2(id="processingdays", style={"color":'white'},className="card-text"),
                      ]
                  ),
                  ],color="secondary"
)
smallcard2=dbc.Card(
                  [
                  dbc.CardHeader(html.H4("Total Claims", style={"font-family": "Arial, Helvetica, sans-serif","color":'white'}, className="card-title")),
                  dbc.CardBody(
                     [
                        html.H2(id="total claims", style={"color":'white'},className="card-text"),
                      ]
                  ),
                  ],color="secondary"
)

smallcard3=dbc.Card(
                  [
                  dbc.CardHeader(html.H4("Total Appeals", style={"font-family": "Arial, Helvetica, sans-serif","color":'white'}, className="card-title")),
                  dbc.CardBody(
                     [
                        html.H2(id="total appeals", style={"color":'white'},className="card-text"),
                      ]
                  ),
                  ],color="secondary"
)

xycard=dbc.Card(
              [
              dbc.FormGroup(
                  [
                      dbc.Label("x-axis",color='light'),
                      dcc.Dropdown(
                          id='x axis',
                          options=[{'label':'Appeal Category' , 'value':'Appeal Category'},
                                   {'label':'Medicare Part' , 'value':'Medicare Part'},
                                   {'label':'Major Procedure Category' , 'value':'Procedure Code'},
                                   {'label':'State' , 'value':'State'}
                                  ],
                          value='Medicare Part',
                          clearable=False
                      ),
                  ]
              ),
              dbc.FormGroup(
                  [
                      dbc.Label("y-axis",color='light'),
                      dcc.Dropdown(
                          id='y axis',
                          options=[{'label':'Claims' , 'value':'Claims'},
                                   {'label':'Approved' , 'value':'Approved'},
                                   {'label':'Denied' , 'value':'Denied'},
                                   {'label':'Processing Days' , 'value':'Processing_Days2'}
                                  ],
                          value='Approved',
                          clearable=False
                      ),
                  ]
              ),
              dbc.FormGroup(
                  [
                  dbc.Button(id='submit_button2',
                              n_clicks=0,color="light", className="mr-1",
                              children='Apply'
                      )
                  ]
              )
              ],
              body=True,
              color='dark'
)

app.layout=dbc.Container(
    [
    html.H1("CUSTOM FILTERS",style={"font-family": "Arial, Helvetica, sans-serif","letter-spacing": 3}),
    html.Hr(),
    dbc.Row(
        [
          dbc.Col(controls,md=5),
          dbc.Col(dcc.Graph(id="approved_denied"),md=7)
        ],
        justify="start",
    ),
    dbc.Row(
        [
        # dbc.Col(xycard,md=6),
        dbc.Col(smallcard3,md=4,sm=5),
        dbc.Col(smallcard1,md=4,sm=5),
        dbc.Col(smallcard2,md=4,sm=5)
        ],
        justify='around',
        style={'marginTop':10}
        # margin=10
    ),
    # html.H1("Dashboard_2",style={"font-family": "Arial, Helvetica, sans-serif","letter-spacing": 3}),
    # html.Hr(),
    # dbc.Row(
    #     [
    #     dbc.Col(xycard,md=5),
    #     # dbc.Col(addcard,md=5)
    #     ],justify='start'
    # ),
    dbc.Row(
           [
           dbc.Col(xycard,md=6),
           ],
           style={'marginTop':30},
           justify='center'
    ),
    dbc.Row(
        [
        dbc.Col(dcc.Graph(id='bar_chart'),md=12),#,style={'height': 1000})
        ],
        style={'marginTop':30},
    ),
    dbc.Row([
            dbc.Col(dcc.Graph(id='geo_map'),md=12)
            ],justify='around',
            style={'marginTop':30},
    ),
    ]
    # fluid=True,
)

@app.callback(
             Output('approved_denied','figure'),
             Output('processingdays','children'),
             Output('total claims','children'),
             Output('total appeals','children'),
             [Input('submit_button','n_clicks')],
             [State('state','value'),
             State('Medicare part','value'),
             State('Appeal category','value'),
             State('Procedure code','value')
             ]
             )
def updatestats(n_clics,statename,medpart,appealC,pc):
    moddf=df
    result={'pie':None,'processingdays':None,'totalclaims':None,'total appeals':None}
    if(statename):
        mod=moddf.loc[moddf['State']==statename[0]]
        for i in statename[1:]:
            mod=pd.concat([mod,moddf.loc[moddf['State']==i]])
        moddf=mod
    if(medpart):
        mod=moddf.loc[df['Medicare Part']==medpart[0]]
        for i in medpart[1:]:
            mod=pd.concat([mod,moddf.loc[moddf['Medicare Part']==i]])
        moddf=mod
    if(appealC):
        mod=moddf.loc[df['Appeal Category']==appealC[0]]
        for i in appealC[1:]:
            mod=pd.concat([mod,moddf.loc[moddf['Appeal Category']==i]])
        moddf=mod
    if(pc):
        mod=moddf.loc[df['Procedure Code']==pc[0]]
        for i in pc[1:]:
            mod=pd.concat([mod,moddf.loc[moddf['Procedure Code']==i]])
        moddf=mod
    approved=len(moddf.loc[moddf['Disposition']==1])
    denied=len(moddf.loc[moddf['Disposition']==0])
    result['total appeals']=str(approved+denied)
    result['pie']={
                   'data':[go.Pie(labels=['Approved','Denied'],values=[approved,denied],hole=.5)],
                   'layout':go.Layout(title='Approved and Denied')
                  }
    average=0
    if(len(moddf)):
        average=int(statistics.median(sorted(moddf['Processing_Days2'])))
    result['processingdays']=str(average)
    total=sum(moddf['Claims'])
    result['totalclaims']=str(total)
    return result['pie'],result['processingdays'],result['totalclaims'],result['total appeals']

# fig = go.Figure(data=go.Choropleth(
#     locations=df['code'],
#     z=df['total exports'].astype(float),
#     locationmode='USA-states',
#     colorscale='Reds',
#     autocolorscale=False,
#     text=df['text'], # hover text
#     marker_line_color='white', # line markers between states
#     colorbar_title="Millions USD"
# ))
@app.callback(
              Output('bar_chart','figure'),
              Output('geo_map','figure'),
              [Input('submit_button2','n_clicks')],
              [State('x axis','value'),
               State('y axis','value')]
              )
def bargraph(n_clicks,xaxis,yaxis):
    xlabel=df[xaxis].unique()
    ylabel=None
    result={}
    if(yaxis == 'Claims'):
        ylabel=[sum(df.loc[df[xaxis]==i]['Claims']) for i in xlabel]
    if(yaxis == 'Approved'):
        ylabel=[sum(df.loc[df[xaxis]==i]['Disposition']) for i in xlabel]
    if(yaxis=='Denied'):
        ylabel=[len(df.loc[(df[xaxis]==i) & (df['Disposition']==0)]) for i in xlabel]
    if(yaxis=='Processing_Days2'):
        ylabel=[]
        for i in xlabel:
            arr=sorted(df.loc[df[xaxis]==i]['Processing_Days2'])
            if(len(arr)):
                ylabel.append(int(statistics.median(arr)))
            else:
                ylabel.append(0)
    if(xaxis=='State'):
        xlabel=[postal[i] for i in xlabel]
    if(yaxis=='Processing_Days2'):
        yaxis='Processing Days'
    if(xaxis=='Procedure Code'):
        xaxis='Major Procedure Category'
    result['bar']={'data':[go.Bar(x=xlabel,y=ylabel)],
                   'layout':{
                              'title_standoff':25,
                              'tickangle':30,
                              'font_family':"Courier New",
                              'xaxis':{'tickfont':{'size':8}},
                              'yaxis':{'title':yaxis,'domain':(0.25,1),'tickfont':{'size':8}},#'domain':(0.25,0.75)
                              'height':600,
                              # 'font':{
                              #         'size':8
                              #        },

                              'title':{'text':xaxis+' vs '+yaxis,'size':40},
                            }
                  }
    if(xaxis=='Major Procedure Category'):
        xaxis='Procedure Code'
    #for geomap
    if(yaxis=='Processing Days'):
        yaxis='Processing_Days2'
    statename=df['State'].unique()
    locationarr=[i.upper() for i in statename]
    zarr=[]
    full=[postal[i] for i in statename]
    if(yaxis == 'Claims'):
        for i in statename:
            total=0
            total=sum(df.loc[df['State']==i]['Claims'])
            zarr.append(total)
    if(yaxis == 'Approved'):
        for i in statename:
            total=len(df.loc[(df['State']==i) & (df['Disposition']==1)])
            zarr.append(total)
    if(yaxis=='Denied'):
        for i in statename:
            total=len(df.loc[(df['State']==i) & (df['Disposition']==0)])
            zarr.append(total)
    if(yaxis=='Processing_Days2'):
        for i in statename:
            arr=sorted(df.loc[df['State']==i]['Processing_Days2'])
            average=0
            if(len(arr)):
                average=int(statistics.median(arr))
            zarr.append(average)
    if(yaxis=='Processing_Days2'):
        yaxis='Processing Days'
    result['geomap']={
            'data':[go.Choropleth(
                locations=locationarr,
                z=zarr,
                locationmode='USA-states',
                colorscale='Reds',
                autocolorscale=False,
                text=full, # hover text
                marker_line_color='white', # line markers between states
                colorbar_title=yaxis
            )],
            'layout':{
                     'title':'Choropleth Map of US- '+yaxis,
                     'geo' : dict(
                                 scope='usa',
                                 projection=go.layout.geo.Projection(type = 'albers usa'),
                                 showlakes=True, # lakes
                                 lakecolor='rgb(255,255,255))'),
                    'height':500,
                    'margin':{"r":0,"t":50,"l":0,"b":0}
            }
           }
    return result['bar'],result['geomap']

@app.callback(
             Output('submit_button','disabled'),
             Output('clear-button','disabled'),
             [Input('state','value'),
             Input('Medicare part','value'),
             Input('Appeal category','value'),
             Input('Procedure code','value')
             ]
             )
def changeButton(SN,MP,AC,PC):
    if((not SN) and (not MP) and (not AC) and (not PC)):
        return True,True
    else:
        return False,False


@app.callback(
             Output('submit_button','n_clicks'),
             Output('state','value'),
             Output('Medicare part','value'),
             Output('Appeal category','value'),
             Output('Procedure code','value'),
             [Input('clear-button','n_clicks')],
             )
def clearall(n_clicks):
    return 1,[],[],[],[]
if __name__ == "__main__":
    app.run_server()
