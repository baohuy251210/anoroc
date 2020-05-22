import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import figure
from dash.dependencies import Input, Output, State
import database
import pandas as pd
import time
from database import dict_alpha_name
from app import app
database_local_status = True
df_country_index = database.get_df_country_index(database_local_status)


def generate_dropdown():
    dframe = df_country_index
    lst = []
    for i in range(len(dframe)):
        lst.append({'label': dframe.iloc[i][1]+', '+dframe.iloc[i][0],
                    'value': dframe.iloc[i][0]})
    return dcc.Dropdown(
        id='country-dropdown',
        options=lst,
        placeholder="Select",
        clearable=False,
        searchable=True,
        value=dframe.iloc[-8][0],
    )


@app.callback(
    [Output('dropdown-output-container', 'className'),
        Output('dropdown-output-header', 'children'),
     Output('dropdown-output-body', 'children'),
     ],
    [Input('country-dropdown-submit', 'n_clicks'),
     Input('country-dropdown-watch', 'n_clicks')],
    [State('country-dropdown', 'value'),
     State('show-checklist', 'value'),
     State('dropdown-output-container', 'className'),
     ]
)
def country_select(submit_clicks, watch_clicks, alpha, checklist, card_class):
    """Handle submit button from country-select

    Arguments:
        n_clicks {[type]} -- [description]
        alpha {[type]} -- [description]
        checklist {[type]} -- [description]
        card_class {[type]} -- [description]

    Returns:
        set card to visible
        Country name -- card header (html friendly)
        country data -- card body (html friendly)
        loader graph -- figure
    """
    if (submit_clicks == None and watch_clicks == None):
        return str(card_class), None, None
    status = database.get_country_live_status(alpha)
    card_body_div = generate_card_body(status)
    return [str(card_class).replace(' d-invisible', ' d-visible'), dict_alpha_name[alpha]['name'], card_body_div]

# @app.callback(
#     Output('dropdown-output', 'children'),
#     [Input('country-dropdown', 'value')])


def generate_country_charts(value, checklist):
    """Input- value: country's alpha

    Arguments:
        value {dcc.graph} -- a dcc graph showing timeline of the country
    """
    if (value == None):
        return "Not done"
    country_name = database.get_quick_country_name(value)
    fig = figure.fig_line_chart(
        country_name, database.get_quick_country_timeline(value), checklist)
    return dcc.Graph(figure=fig, style={'width': '100%', 'height': '100%',
                                        'fontFamily': 'Roboto Mono', })


@app.callback(
    Output('output_live_table', 'children'),
    [Input('btn_live_table', 'n_clicks')]
)
def generate_live_table(n_clicks):
    """
    Function to return live table dash_table.DataTable
    """
    df = database.get_df_all_country_status(database_local_status)
    df = df.drop(columns='alpha2')
    df['last_update'] = pd.to_datetime(df['last_update']).astype(str)
    df = df.rename(columns={"name": "Country", "cases": "Infected", 'deaths': 'Deaths', 'recovered': 'Recovered',
                            'last_update': 'Last Update GMT+0'})
    df = df.sort_values('Infected', ascending=False)
    return dash_table.DataTable(
        id='live-table',
        columns=[
            {'name': i, 'id': i} for i in df.columns
        ],
        data=df.to_dict('records'),
        style_table={'height': 'auto', 'margin': 'auto',
                     'overflowY': 'auto', 'overflowX': 'hidden'},
        page_action="native",
        page_size=20,

        # style_as_list_view=True,

        style_cell={
            'whitespace': 'normal',
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
            'fontSize': 15,
            'textAlign': 'center',
            'color': 'rgba(0,0,0,0.87)',
            'fontFamily': 'Jost',
            'paddingLeft': '0px',
            'paddingRight': '0px',

        },
        style_cell_conditional=[
            {'if': {'column_id': 'Country'},
             'width': '35%', 'textAlign': 'left', 'paddingLeft': '20px', },
            {'if': {'column_id': 'Last Update GMT+0'},
             'paddingRight': '20px',
             'width': '20%'},
        ],
        style_data_conditional=[
            {'if': {'column_id': 'Last Update GMT+0'},
                'fontSize': 11, 'paddingRight': '20px',
             'width': '20%'},
        ],

    )


'''
Layout generator for controller:

'''


def generate_card_body(status):
    """Generate a container for selected country card

    Arguments:
        status {Tuple} -- (cases, deaths, recovered)
        graph {dcc.Graph} -- timeline graph

    Returns:
        Html.Div -- contains content for card-body
    """
    return html.Div(className='container', children=[
        # html.Div(className='h5 text-center my-2',
        #  children='Current status:'),
        html.Div(className='columns', children=[  # status cards
            html.Div(className='column col-3 col-mx-auto', children=[
                html.Span(className='label label-primary', children=[
                    "Infected:"
                ]),
                html.Span(className='label label-secondary', children=[
                    status[0]
                ])
            ]),
            html.Div(className='divider-vert'),
            html.Div(className='column col-3 col-mx-auto', children=[
                html.Span(className='label label-primary', children=[
                    "Deceased:"
                ]),
                html.Span(className='label label-secondary', children=[
                    status[1]
                ])
            ]),
            html.Div(className='divider-vert'),
            html.Div(className='column col-3 col-mx-auto', children=[
                html.Span(className='label label-primary', children=[
                    "Recovered:"
                ]),
                html.Span(className='label label-secondary', children=[
                    status[2]
                ])
            ]),
        ]),
        html.Div(className='divider'),
        html.Button(id='graph-btn-timeline', className='btn btn-primary', children=[
            'Timeline'
        ]),
        html.Div(className='columns', children=[  # charts
            html.Div(className='column col-12', children=[
                dcc.Loading(id='graph-loader', type='circle', color='#5755d9', style={'paddingTop': '50px'}, children=[

                ])
            ])
        ]),
    ], style={'fontFamily': 'Roboto Slab'})


@app.callback(
    Output('graph-loader', 'children'),
    [Input('graph-btn-timeline', 'n_clicks')],
    [State('country-dropdown', 'value'),
     State('show-checklist', 'value')]
)
def generate_timeline_graph(btn_clicks, alpha, checklist):
    """Generate timeline graph based on btn click

    Arguments:
        btn_clicks {[type]} -- [description]
        alpha {[type]} -- [description]
        checklist {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    if (btn_clicks == None):
        return
    elif len(checklist) == 0:
        return html.Span(className='label label-error', children="Please choose at least one type")
    else:
        return generate_country_charts(alpha, checklist)
