import database
import psycopg2
import figure
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
data_updated_time = "version test"
# data_updated_time = data_rebase.update_check()
# REBASED Stuffs below:

df_rebased_all = pd.read_csv('./data_rebase/country_all_new_status.csv', encoding='utf-8',
                             keep_default_na=False, na_values=['__'])
df_rebased_all['last_update'] = pd.to_datetime(df_rebased_all['last_update'])
df_rebased_all = df_rebased_all.drop(columns='country')
df_rebased_all.columns = ['Country', 'Infected Cases',
                          'Deaths', 'Total Recovered', 'Last Update (UTC)']

df_country_index = pd.read_csv('./data_rebase/country_alpha_index.csv',
                               keep_default_na=False, na_values=['__'], encoding='utf-8')
# print(df_country_index)
'''
-----------------------
Dash Core/Html component generators
'''


def generate_dropdown(dframe):
    lst = []
    for i in range(len(dframe)):
        lst.append({'label': dframe.iloc[i][0]+', '+dframe.iloc[i][1],
                    'value': dframe.iloc[i][1]})

    # print(lst)
    return dcc.Dropdown(
        id='country-dropdown',
        options=lst,
        placeholder="Select country to inspect",
        clearable=False,
        searchable=True,
        value=dframe.iloc[-8][1],  # United States of America
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
def update_output_sql(value):
    alpha, name = database.get_country_from_alpha(value)

# @app.callback(
#     Output('dropdown-output', 'children'),
#     [Input('country-dropdown', 'value')])
# def update_output(value):
#     newdf = df_rebased_all[df_rebased_all['Country'] == value].astype(str)

#     dict_name_alpha = pd.read_csv('./data_rebase/country_alpha_index.csv',
#                                   index_col='name', keep_default_na=False, na_values=['__'], encoding='utf-8').to_dict('index')
#     country_alpha = dict_name_alpha[value]['alpha2']
#     country_url = './data_rebase/country-timeline/{}.csv'.format(country_alpha)

#     df_country = pd.read_csv(
#         country_url, encoding='utf-8', keep_default_na=False, na_values=['__'])
#     df_country = df_country.drop(columns='country')
#     df_country['last_update'] = pd.to_datetime(df_country['last_update'])

#     fig = figure.fig_line_chart(value, df_country)
#     # fig = fig_bar_chart(value, df_country)
#     return html.Div([dash_table.DataTable(
#         id='selected',
#         columns=[{'name': i, 'id': i} for i in newdf.columns],
#         style_cell={
#             'whitespace': 'normal',
#             'minWidth': '130px', 'width': '130px', 'maxWidth': '130px',
#             'fontSize': 15,
#             'textAlign': 'center',
#             'color': 'rgba(0,0,0,0.87)',
#             'fontFamily': 'Jost'
#         },
#         style_cell_conditional=[
#             {'if': {'column_id': 'Country'},
#              'width': '23%'},
#             {'if': {'column_id': 'Infected'},
#              'width': '10%'},

#         ],
#         data=newdf.to_dict('records')
#     ),
#         dcc.Graph(figure=fig, style={'marginTop': '25px', 'width': '100%'})
#     ]
#     )


'''
Helper Function SQL
'''

if __name__ == '__main__':
    # Only set False if deploy on heroku:
    app.run_server(debug=False)
