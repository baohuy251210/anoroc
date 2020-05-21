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
-----------------------
Data Frame (pandas) Stuff
'''

data_updated_time = 'version test1'
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
            active_tab="tab_live",
        ),
        html.Div(id='content'),
    ]
)

"""
-----------------------
App.py layouts part
"""

app.layout = \
    html.Div(id='container', className='container',
             children=[
                 html.Div(className='columns bg-gray', children=[
                     html.Div(className='column col-12', children=[
                         html.Header(className='navbar', children=[
                             html.Section(className='navbar-section', children=[
                                 html.A('Real-time Map', href='https://coronavirus.jhu.edu/map.html',
                                        className='btn btn-link'),
                                 html.A('COVID-19 API', href='https://covid19-api.org/',
                                        className='btn btn-link', style={'paddingLeft': '40px'})
                             ]),  # navbar sec 1
                             html.Section(className='navbar-center', children=[
                                 html.Img(
                                     src='/assets/logo-brand.png', style={'height': '80px'})
                             ]),
                             html.Section(className='navbar-section', children=[
                                 html.A(
                                     'View Changelogs and Code on', href='https://github.com/baohuy251210/anoroc', className='btn btn-link'),
                                 html.A(href='https://github.com/baohuy251210/anoroc', children=[
                                     html.Img(
                                        src='/assets/GitHub_Logo.png', style={'height': '32px'}),
                                 ])

                             ])
                         ], style={'fontWeight': '600', 'paddingLeft': '50px', 'paddingRight': '50px'})  # navbar style
                     ])
                 ])


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
                'width': '80%',
                'padding': '27px',
                'fontFamily': 'Roboto',
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
                                       'display': 'inline-block',
                                       'padding': '20px',
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
