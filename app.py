from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
import dash_table
import data_rebase
import os
from dash.dependencies import Input, Output, State
'''
Version 0.5 TODO:
    *offline css file (not codepen.io) [x]
    *fix curacao and cote divoire name [x]
    *heroku scheduler [ ]
    *retouch css, bootstrap [ ]
'''

'''
-----------------------
Data Frame (pandas) Stuff
'''

# ataprocess.update_csv_jhu()+" MDT"
# data_updated_time = "version test"
data_updated_time = data_rebase.update_check()
# REBASED Stuffs below:

df_rebased_all = pd.read_csv('./data_rebase/country_all_new_status.csv', encoding='utf-8',
                             keep_default_na=False, na_values=['__'])
df_rebased_all['last_update'] = pd.to_datetime(df_rebased_all['last_update'])
df_rebased_all = df_rebased_all.drop(columns='country')
df_rebased_all.columns = ['Country', 'Infected Cases',
                          'Deaths', 'Total Recovered', 'Last Update (UTC)']

df_country_index = pd.read_csv('./data_rebase/country_alpha_index.csv',
                               keep_default_na=False, na_values=['__'], encoding='utf-8')
# print(df_rebased_all)
'''
-----------------------
Dash Core/Html component generators
'''


def generate_dropdown(dframe):
    lst = []
    for i in range(len(dframe)):
        lst.append({'label': dframe.iloc[i][0]+', '+dframe.iloc[i][1],
                    'value': dframe.iloc[i][0]})
    # print(lst)
    return dcc.Dropdown(
        id='country-dropdown',
        options=lst,
        placeholder="Select country to inspect",
        clearable=False,
        searchable=True,
        value=dframe.iloc[-8][0],  # United States of America
        style={
            'fontFamily': 'Jost',
            'display': 'inline-block',
            'textAlign': 'center',
            'fontStyle': 'bold',
            'margin': '0 auto',
            'color': 'rgba(0,0,0,0.6)',
            'width': '40%',
            'position': 'relative',
            'verticalAlign': 'middle',
            # 'fontFamily': 'Roboto',
        }
    )


def generate_table(dataframe):
    return html.Table(
        [
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(str(dataframe.iloc[i][col])) for col in dataframe.columns
                ]) for i in range(len(dataframe))
            ]),
        ], style={
            'marginTop': '3px',
            'color': 'rgba(0,0,0,0.87)',

        })


# def generate_dropdown

"""
-----------------------
App.py layouts part
"""
external_stylesheets = [
    './assets/stylesheet.css']
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Anoroc Monitor'

app.layout = html.Div(id='container', className='parent',
                      children=[
                          html.H1(children='ANOROC - Live Covid19 Monitor',
                                  style={
                                      'marginBottom': '5px',
                                      'marginTop': '12px',
                                      'verticalAlign': 'center',
                                      'textAlign': 'center'
                                  },
                                  ),
                          html.H6(['last updated from anoroc: '+str(data_updated_time)+'(GMT +0)'],
                                  style={
                              'textAlign': 'right',
                                      'fontSize': '13px',
                                      'fontFamily': 'Arvo',
                                      'fontStyle': 'italic',
                                      'marginTop': '1px',
                                      'paddingRight': '250px',
                          }),
                          html.H6([html.A("Version 0.3 Changelog", href='https://github.com/baohuy251210/anoroc')],
                                  style={
                                      'textAlign': 'right',
                                      'fontSize': '13px',
                                      'fontFamily': 'Arvo',
                                      'fontStyle': 'italic',
                                      'marginTop': '1px',
                                      'paddingRight': '250px',
                          },

                          ),
                          html.H6(children="Historical data for graphs is updated every 24 hours",
                                  style={
                                      'textAlign': 'right',
                                      'fontSize': '13px',
                                      'fontStyle': 'italic',
                                      'marginBot': '14px',
                                      'paddingRight': '250px',
                                      'fontFamily': 'Roboto Condensed'
                                  },
                                  ),
                          html.Br(),
                          html.H5('Select Country to Inspect:', style={
                              'textAlign': 'center',
                              'fontFamily': 'Jost'
                          }),
                          generate_dropdown(df_country_index),
                          html.Div(id='dropdown-output',
                                   style={
                                       'marginTop': "10px",
                                       'fontFamily': 'Roboto',
                                       'width': '90%',
                                       'overflow': 'auto',
                                       'textAlign': 'center',
                                       'verticalAlign': 'center',
                                       'display': 'inline-block'
                                   }),

                          html.H5('Live Updated Data: '+str(data_updated_time)+'(GMT +0)', style={
                              'marginBottom': '0px',
                              'fontWeight': '400',
                              'marginTop': '5px',
                              'fontFamily': 'Jost',
                              #   'border-top-left-radius': '6px',
                              #   'border-top-right-radius': '6px',
                              'borderTop': '2px solid #5f7481',
                              'textAlign': 'center',
                          }),

                          # Full table:
                          html.Div(generate_table(df_rebased_all), style={
                              'verticalAlign': 'center',
                              'margin': '10px auto',
                              'overflow': 'auto',
                              'height': '75%',
                              'width': '75%'
                          }),



                          html.Footer(["Data is sourced from ",
                                       html.A('John Hopkins CSSE',
                                              href='https://github.com/CSSEGISandData/COVID-19', style={'color': '#ffdc65'}),
                                       html.Br(),
                                       " updated from a free ",
                                       html.A('COVID19-API',
                                              href='https://covid19-api.org/', style={'color': '#ffdc65'}),
                                       html.Br(),
                                       "A tracker monitor for COVID-19, Created by ",
                                       html.A("baohuy251210@Github/Anoroc",
                                              href='https://github.com/baohuy251210/anoroc', style={'color': '#ffdc65'}),
                                       html.Br(),
                                       "More improvements will be added :)"


                                       ],
                                      style={
                              #   'fontStyle': 'italic',
                              'marginTop': '30px',
                              'color': '#FFFFFF',
                              'backgroundColor': '#344955',
                              'fontFamily': 'Roboto Condensed',
                              'fontWeight': '400'
                          })
                      ], style={
                          'borderTop': '30px solid #344955',
                          'verticalAlign': 'middle',
                          'textAlign': 'center',
                          'position': 'absolute',
                          'width': '100%',
                          'height': '100%',
                          'top': '0px',
                          'left': '0px',
                      }
                      )


'''
---------------
Handling callbacks:
'''


@app.callback(
    Output('dropdown-output', 'children'),
    [Input('country-dropdown', 'value')])
def update_output(value):
    newdf = df_rebased_all[df_rebased_all['Country'] == value].astype(str)

    dict_name_alpha = pd.read_csv('./data_rebase/country_alpha_index.csv',
                                  index_col='name', keep_default_na=False, na_values=['__'], encoding='utf-8').to_dict('index')
    country_alpha = dict_name_alpha[value]['alpha2']
    country_url = './data_rebase/country-timeline/{}.csv'.format(country_alpha)

    df_country = pd.read_csv(
        country_url, encoding='utf-8', keep_default_na=False, na_values=['__'])
    df_country = df_country.drop(columns='country')
    df_country['last_update'] = pd.to_datetime(df_country['last_update'])

    fig = fig_line_chart(value, df_country)
    # fig = fig_bar_chart(value, df_country)
    return html.Div([dash_table.DataTable(
        id='selected',
        columns=[{'name': i, 'id': i} for i in newdf.columns],
        style_cell={
            'whitespace': 'normal',
            'minWidth': '130px', 'width': '130px', 'maxWidth': '130px',
            'fontSize': 15,
            'textAlign': 'center',
            'color': 'rgba(0,0,0,0.87)',
            'fontFamily': 'Jost'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Country'},
             'width': '23%'},
            {'if': {'column_id': 'Infected'},
             'width': '10%'},

        ],
        data=newdf.to_dict('records')
    ),
        dcc.Graph(figure=fig, style={'marginTop': '25px', 'width': '100%'})
    ]
    )


'''
Helper Function to generate figures
'''


def fig_line_chart(value, df_country):
    fig = go.Figure()
    df_country['newcases'] = df_country['cases'].diff(1)
    df_country['newrecovered'] = df_country['recovered'].diff(1)
    df_country['newdeaths'] = df_country['deaths'].diff(1)
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=('Total Confirmed', 'Daily Confirmed'
                                        ),
                        row_heights=[0.5, 0.5],
                        shared_xaxes=True,
                        vertical_spacing=0.3
                        )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['cases'],
                             mode='lines',
                             legendgroup='infected',
                             name='Infected',
                             line=dict(color='tomato')),
                  row=1, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['recovered'],
                             mode='lines',
                             legendgroup='recovered',
                             name='Recovered',
                             line=dict(color='forestgreen')),
                  row=1, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['deaths'],
                             mode='lines',
                             legendgroup='deceased',
                             name='Deceased',
                             line=dict(color='firebrick', width=1)),
                  row=1, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['newcases'],
                             mode='lines',
                             legendgroup='infected',
                             name='Infected - Daily',
                             line=dict(color='tomato', width=1.5)),
                  row=2, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['newrecovered'],
                             mode='lines',
                             legendgroup='recovered',
                             name='Recovered - Daily',
                             line=dict(color='forestgreen', width=1.5)),
                  row=2, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['newdeaths'],
                             mode='lines',
                             legendgroup='deceased',
                             name='Deceased - Daily',
                             line=dict(color='firebrick', width=1.5)),
                  row=2, col=1
                  )
    # fig.update_traces(hoverinfo='x+y', stackgroup='one')
    fig.update_layout(hovermode='x', autosize=True,
                      height=800,
                      font=dict(
                          family="Jost",
                          size=12,
                          color="#000000"
                      ),
                      title={
                          'text': value+': Reported Infected, Deaths and Recovered',
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'},
                      xaxis_title='Timeline',
                      yaxis_title='Reported Counts',
                      xaxis_range=[datetime.datetime(2020, 4, 10),
                                   datetime.datetime(2020, 5, 20)],
                      yaxis=dict(autorange=True, fixedrange=False),
                      xaxis_rangeslider_visible=True, xaxis_rangeslider_thickness=0.05
                      )

    fig.update_layout(hovermode='x', autosize=True,
                      height=800,
                      font=dict(
                          family="Jost",
                          size=12,
                          color="#000000"
                      ),
                      title={
                          'text': value+': Reported Infected, Deaths and Recovered',
                          'y': 0.95,
                          'x': 0.2,
                          'xanchor': 'center',
                          'yanchor': 'top'},
                      xaxis_title='Timeline',
                      yaxis_title='Reported Counts',
                      xaxis_range=[datetime.datetime(2020, 4, 10),
                                   datetime.datetime(2020, 5, 20)],
                      yaxis=dict(autorange=True, fixedrange=False),
                      xaxis_rangeslider_visible=True, xaxis_rangeslider_thickness=0.1
                      )

    fig.update_xaxes(
        # rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="7d", step="day",
                     stepmode="backward"),
                dict(count=21, label="3week", step="day",
                     stepmode="backward"),
                dict(count=1, label="1m", step="month",
                     stepmode="backward"),
                dict(count=3, label="3m", step="month",
                     stepmode="backward"),
                dict(step="all")
            ]),

        ))
    fig.update_yaxes(nticks=10)
    return fig


if __name__ == '__main__':
    # Only set False if deploy on heroku:
    app.run_server(debug=True)

