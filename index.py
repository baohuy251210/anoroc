import database
import psycopg2
import figure
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os
from dash.dependencies import Input, Output, State
import controller
from app import app
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

data_updated_time = 'version test'
'''
-----------------------
LAYOUT:
'''
tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Live Table", tab_id="tab_live"),
                dbc.Tab(label="Select Country", tab_id="tab_select"),
            ],
            id='tabs',
            active_tab="tab_select",
        ),
        html.Div(id='content'),
    ]
)

"""
-----------------------
App.py layouts part
"""

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
                          tabs,

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
BOOTSTRAP LAYOUT:
'''

tab_live_content = dbc.Card(
    dbc.CardBody(
        [
            # generate table on click
            dbc.Button('Update Database', color='info',
                       id='btn_live_table', className='btn'),
            html.Div(id='output_live_table', style={
                'verticalAlign': 'center',
                'margin': '10px auto',
                'overflow': 'auto',
                'height': '75%',
                'width': '75%'
            }),
        ]
    ),
    className='tab'
)

tab_select_content = dbc.Card(
    dbc.CardBody(
        [
            controller.generate_dropdown(controller.df_country_index),
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
        ]
    ),
    className='tab',
)


@app.callback(Output('content', 'children'),
              [Input('tabs', 'active_tab')])
def switch_tab(tab_name):
    if tab_name == 'tab_live':
        return tab_live_content
    elif tab_name == 'tab_select':
        return tab_select_content
    return html.P("ERROR: how did you do this? >_<...")


'''
Helper Function SQL
'''

if __name__ == '__main__':
    # Only set False if deploy on heroku:
    app.run_server(debug=True)
