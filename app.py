
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df = df[~df.GEO.str.contains('Euro')]
df = df[~df.UNIT.str.contains('Chain')]
df = df.sort_values('GEO',kind='mergesort')

available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.H1('Macroeconomic Indicators',style={'textAlign': 'center'}),
#first graph
    html.Div([
        html.H2('Graph 1: Find relationships between macro indicators (choose two variables and year below)'),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '45%', 'display': 'inline-block', 'padding':20}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '45%', 'float': 'right', 'display': 'inline-block', 'padding':20})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),

#second graph        
    html.Div([
        html.H2('Graph 2: see time-trend of an indicator (choose country and variable below)'),
        html.Div([
            dcc.Dropdown(
                id='country-value',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Albania'
            )
        ],
        style={'width': '45%', 'display': 'inline-block', 'padding':20}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            )
        ],style={'width': '45%', 'float': 'right', 'display': 'inline-block', 'padding':20})
    ],style={'marginTop': '80'}),
    dcc.Graph(id='indicator-graphic2'),
],style={'width':'95%','display': 'inline-block', 'padding':'20','step':'1'}
)

#callback first graph
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 90, 'b': 80, 't': 10, 'r': 20},
            hovermode='closest'
        )
    }

#callback second graph
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country-value', 'value'),
    dash.dependencies.Input('yaxis-column2', 'value')])
def update_graph(country_value, yaxis_column_name2, ):
    dff = df[df['GEO'] == country_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == yaxis_column_name2]['TIME'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name2]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name2]['GEO'],
            mode='lines+markers',
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Time',
                'type': 'linear',
                'dtick': '1'
            },
            yaxis={
                'title': yaxis_column_name2,
                'type': 'linear',
            },
            margin={'l': 90, 'b': 40, 't': 10, 'r': 20},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

