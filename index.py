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
---------------
Web DESIGN:
'''
page_header = html.Div(className='columns bg-gray', children=[
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
                    src='/assets/logo-brand.png', style={'height': '70px'})
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

page_toasts_news = html.Div(className='toast toast-primary', children=[
    html.Button(className='btn btn-clear float-right'),
    "Welcome to Anoroc Explorer! ",
    "Check the github page for news"
])
page_modal_news = html.Div(className='modal modal-sm active', children=[
    html.Div(className='modal-container', children=[
        html.Div(className='modal-header', children=[
            html.A(href='#close', className='btn btn-clear float-right'),
            html.Div(className='modal-title h5',
                     children=['Welcome to Anoroc Explorer 1.0'])
        ]),
        html.Div(className='modal-body', children=[
            html.Div(className='content', children=[
                "Check out new contents and supports via my Github"])
        ])
    ])
])

"""
-----------------------
App.py layouts part
"""

app.layout = \
    html.Div(id='container', className='container',
             children=[page_header,

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
Helper Function SQL
'''

if __name__ == '__main__':
    # Only set False if deploy on heroku:
    app.run_server(debug=True)
