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
page_modal_news = html.Div(id='modal-main', className='modal modal-sm active', children=[
    html.Div(id='modal-container', className='modal-container', children=[
        html.Div(className='modal-header', children=[
            html.A(id='modal-news-close', href='#',
                   className='btn btn-clear float-right'),
            html.Div(className='modal-title h5',
                     children=['Welcome to Anoroc Explorer 1.0'])
        ]),
        html.Div(className='modal-body', children=[
            html.Div(className='content', children=[
                "Check out new contents and supports via my Github"])
        ])
    ])
])

column_select = html.Div(id='dropdown-input-container', className='card d-hide', children=[
    html.Div(className='card-header', children=[
        html.Div('COVID Data Explorer', className='card-title h4 text-left'),
        html.Div("Watch the trends",
                 className='card-subtitle text-gray text-left'),
    ]),
    html.Div(className='card-body m-2', children=[
        "Select Country:",
        controller.generate_dropdown(),
        html.Div(className='divider'),
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
    html.Div(className='column col-12 col-auto', children=[
        html.Div(id='dropdown-output-container', className='card d-hide text-dark', children=[

            html.Div(id='dropdown-output-header', className='card-header h3', children=[
            ]),

            html.Div(id='dropdown-output-body', className='card-body', children=[
            ])
        ])
    ])


html_linebreak = html.Div(className='columns', children=[])


def html_div_right(div_children):
    return html.Div(className='container', children=[
        html.Div(className='columns', children=[
            html.Div(className='column col-3 col-ml-auto', children=[
                    div_children
                    ])
        ])
    ])


def html_div_select_country(column1, column2):
    return html.Div(className='columns m-2 py-2', children=[
        html.Div(className='column col-4', children=[
            column1,
        ]),
        html.Div(className='column col-8', children=[
            column2,
        ])
    ])


"""
-----------------------
App.py layouts part
"""

app.layout = \
    html.Div(id='app-layout', className='container bg-gray',
             children=[page_header,
                       #    page_toasts_news,
                       #    modal,
                       page_modal_news,
                       html_div_select_country(
                           column_select, column_data),
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
        return {'display': 'none'}, 'modal modal-sm', str(input_class).replace(' d-hide', '')


js_string = """this.document.getElementById('toasts-btn-close').onclick = function() {
        this.document.getElementById('toasts-news').style.display = "none";
        console.log("btn toasts clicked");
        """


'''
Helper Function SQL
'''

if __name__ == '__main__':
    # Only set False if deploy on heroku:
    app.run_server(debug=True)
