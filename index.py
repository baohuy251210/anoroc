import visdcc
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

                html.A(id='btn-home', href='#home', children=[
                    html.Img(
                        src='/assets/logo-brand.png', style={'height': '50px'})
                ])
            ]),
            html.Section(className='navbar-section', children=[
                html.A(
                    'View Code on', href='https://github.com/baohuy251210/anoroc', className='btn'),
                html.A(href='https://github.com/baohuy251210/anoroc', children=[
                    html.Img(
                        src='/assets/GitHub_Logo.png', style={'height': '32px'}),
                ])

            ])
        ], style={'fontWeight': '600', 'paddingLeft': '50px', 'paddingRight': '50px'})  # navbar style
    ])
])


column_select = html.Div(id='dropdown-input-container', className='card', children=[
    html.Div(className='card-header', children=[
        html.Div('COVID Data Explorer', className='card-title h3 text-left'),
        html.Div("Watch the trends",
                 className='card-subtitle text-gray text-left'),
    ]),
    html.Div(className='card-body m-2', children=[
        html.Div(className='h6', children='Select country:'),
        controller.generate_dropdown(),
        html.Button('Watch', className='btn btn-secondary m-2',
                    id='country-dropdown-watch'),
        html.Div(className='divider'),
        html.Div(className='h6', children='Select status type(s):'),
        dcc.Checklist(id='show-checklist',
                      options=[
                          {'label': ' Show Infected ', 'value': 'infected'},
                          {'label': ' Show Deaths ', 'value': 'deaths'},
                          {'label': ' Show Recovered ', 'value': 'recovered'}
                      ],
                      value=['infected', 'deaths', 'recovered'],
                      #   className='form-group',
                      labelStyle={'display': 'block',
                                  'marginBottom': '.4rem'},

                      )
    ]),
    html.Div(className='card-footer m-2', children=[
        html.Button('Submit', className='btn btn-primary',
                    id='country-dropdown-submit')
    ])
])

column_data = \
    html.Div(className='column col-12 col-mx-auto', children=[
        html.Div(id='dropdown-output-container', className='card text-dark d-invisible', children=[

            html.Div(id='dropdown-output-header', className='card-header h3', children=[
            ]),

            html.Div(id='dropdown-output-body', className='card-body', children=[
            ])
        ])
    ])


div_hero =\
    html.Div(id='hero-container', className='hero bg-gray section', children=[
                html.H2('Anoroc Explorer', style={'marginBottom': '30px'}),
                html.H5(['Monitor your updated ', html.U(
                    'COVID-19'), ' Data within seconds'], style={'marginBottom': '30px'}, className='text-light text-dark'),
                html.P([
                    html.A(id='btn-start', className='btn btn-secondary btn-lg mr-2',
                           href='#selector', children="Explore"),
                    html.A(
                        'Github', href='https://github.com/baohuy251210/anoroc', className='btn btn-primary btn-lg')
                ]),
        html.P(className='text-gray text-large', children=["Version 1.0"])

    ])

div_introduction =\
    html.Div(id='intro', className='section hero hero-sm text-center text-light bg-primary', children=[
        html.H2('Introduction'),
        html.Div(className='columns', children=[
            html.Div(className='column col-6 col-sm-12 col-mx-auto text-center', children=[
                html.P(className='text-secondary', children=[
                    html.Strong('Anoroc '),
                    "is a Python Dash project created to monitor the daily updated data of multiple country",
                    ". It's nothing really but my simple interest just to make this website :)",
                ]),
                html.P(className='text-secondary', children=[
                    "Powered by ", html.Strong(
                        'Dash, Plotly, Spectre CSS, Github and Heroku'),
                ]),
            ])
        ]),
        # cards ::>
        html.Div(className='columns', children=[
            html.Div(className='column col-3 col-xs-8 col-mx-auto text-dark', children=[
                html.Div(className='card text-center', children=[
                    html.Div(className='card-header h3',
                             children='Up-to-date'),
                    html.Div(
                        className='card-body', children='Country status are updated every 2 hours, fetching data from JHU CSSE')
                ], style={'padding': '0.5rem', 'border': '0'})
            ]),
            html.Div(className='column col-3 col-xs-8 col-mx-auto text-dark', children=[
                html.Div(className='card text-center', children=[
                    html.Div(className='card-header h3',
                             children='Interactive'),
                    html.Div(
                        className='card-body', children='Allows searching country, interacting with graphs and data types')
                ], style={'padding': '0.5rem', 'border': '0'})
            ]),
            html.Div(className='column col-3 col-xs-8 col-mx-auto text-dark', children=[
                html.Div(className='card text-center', children=[
                    html.Div(className='card-header h3',
                             children='Speedy'),
                    html.Div(
                        className='card-body', children='To provide the best experiences, Anoroc prioritizes lightweight data loads')
                ], style={'padding': '0.5rem', 'border': '0'})
            ])
        ], style={'marginLeft': '50px', 'marginRight': '50px', 'marginBottom': '50px'}),
        html.Div(className='columns', children=[
            html.Div(className='column col-5 col-lg-12 col-mx-auto', children=[
                html.A(id='btn-start-2', className='h1 btn btn-secondary btn-lg mr-2',
                       href='#selector', children="Start Explore"),
            ])
        ])

    ])


def html_div_select_country(column1, column2):
    return html.Div(className='columns m-2 py-2', children=[
        html.Div(className='column col-4', children=[
            column1,
        ], style={'padding': '24px'}),
        html.Div(className='column col-8', children=[
            column2,
        ])
    ])


"""
-----------------------
App.py layouts part
"""
page_home_layout = html.Div([div_hero, div_introduction])

page_country_select = html.Div(className='section bg-gray', children=[
                               html_div_select_country(column_select, column_data)], style={'borderBottom': '30px'})


app.layout = \
    html.Div(id='app-layout', className='bg-gray',
             children=[page_header,
                       dcc.Location(id='url', refresh=False),
                       html.Div(id='page-content')
                       ], style={
                 'verticalAlign': 'middle',
                 'textAlign': 'center',
                 'width': '100%',
                 'height': 'auto',
                 'top': '0px',
                 'left': '0px',
             }
             )

'''
DASH cannot load js correctly so...
-------------
LAYOUT callbacks (Design):
'''


@app.callback(
    [Output("modal-container", "style"),
     Output('modal-main', 'className'),
     Output('dropdown-input-container', 'className')],
    [Input("modal-news-close", "n_clicks")],
    [State("modal-container", "style"),
     State('dropdown-input-container', 'className')]
)
def close_modal(n_clicks, prop, input_class):
    if (n_clicks == None):
        return {'display': 'block'}, 'modal modal-sm active', str(input_class)
    else:
        return {'display': 'none'}, 'modal modal-sm', str(input_class).replace(' d-invisible', '')


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'hash')]
)
def display_page(hash):
    if hash == None:
        return page_home_layout
    elif hash == '#selector':
        return page_country_select
    else:
        return page_home_layout


'''
Helper Function SQL
'''

if __name__ == '__main__':
    # Only set False if deploy on heroku:
    app.run_server(debug=True)
