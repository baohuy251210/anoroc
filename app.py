import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime
import dataprocess
import dash_table
import os
from dash.dependencies import Input, Output, State
'''
-----------------------
Data Frame (pandas) Stuff
'''
data_updated_time = dataprocess.update_csv_jhu()+" MDT"
df = pd.read_csv('./data/jhu_sorted.csv', encoding='cp1252')
df.columns = ['Country', 'Infected', 'New Infected', 'Total Deaths', 'New Deaths',
              'Total Recovered', 'New Recovered']
df_search = pd.read_csv('./data/jhu.csv', encoding='cp1252')
df_search.columns = ['Country', 'Infected', 'New Infected', 'Total Deaths', 'New Deaths',
                     'Total Recovered', 'New Recovered']


'''
-----------------------
Dash Core/Html component generators
'''


def generate_dropdown(dframe):
    lst = []
    for i in range(len(dframe)):
        lst.append({'label': dframe.iloc[i][0],
                    'value': dframe.iloc[i][0]})
    # print(lst)
    return dcc.Dropdown(
        id='country-dropdown',
        options=lst,
        placeholder="Select country to inspect",
        clearable=False,
        searchable=True,
        value=df.iloc[0][0],
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
                    html.Td('+'+str(dataframe.iloc[i][col])) if str(col).startswith('New')
                    else html.Td(str(dataframe.iloc[i][col]))
                    for col in dataframe.columns
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
# external_stylesheets = ['https://codepen.io/baohuy251210/pen/KKdGQep.css']
external_stylesheets = [
    'https://codepen.io/baohuy251210/pen/OJyBYoq.css']
# external_scripts = ['https://codepen.io/zavoloklom/pen/IGkDz.js']
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Anoroc Monitor'

app.layout = html.Div(id='container', className='parent',
                      children=[

                          html.H1(children='ANOROC - Covid19 Monitor',
                                  style={
                                      'marginBottom': '5px',
                                      'marginTop': '12px',
                                      'verticalAlign': 'center',
                                      'textAlign': 'center'
                                  },
                                  ),
                          html.H4(children="Last updated: " + data_updated_time + ".",
                                  style={
                                      'textAlign': 'center',
                                      'marginTop': '5px',

                                  },
                                  ),
                          html.Br(),
                          html.H5('Select Country to Inspect:', style={
                              'textAlign': 'center',
                          }),
                          generate_dropdown(df_search),
                          html.Div(id='dropdown-output',
                                   style={
                                       'marginTop': "10px",
                                       'fontFamily': 'Roboto',
                                       'width': '75%',
                                       'overflow': 'auto',
                                       'textAlign': 'center',
                                       'verticalAlign': 'center',
                                       'display': 'inline-block'
                                   }),

                          html.H5('Collected Data:', style={
                              'marginBottom': '0px',
                              'marginTop': '12px',
                              'textAlign': 'center',
                          }),

                          # Full table:
                          html.Div(generate_table(df), style={
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
                                       " through a free API from Kyle Redelinghuys ",
                                       html.A('COVID19API',
                                              href='covid19api.com', style={'color': '#ffdc65'}),
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
    newdf = df_search[df_search['Country'] == value]
    slug_name = dataprocess.index_name_slug(value)
    countryUrl = './data/countries-total-dayone/{}.csv'.format(slug_name)
    df_country = pd.read_csv(countryUrl, encoding='cp1252')
    print(df_country)
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
    ), html.Label("selected " + slug_name, style={"marginTop": "50px"})]
    )


if __name__ == '__main__':
    # Only set False if deploy on heroku:
    app.run_server(debug=True)
