import dash
import dash_core_components as dcc
import dash_html_components as html
import figure
from dash.dependencies import Input, Output, State
import database
import pandas as pd
from database import dict_alpha_name
from app import app
df_country_index = pd.read_csv('./data_rebase/country_alpha_index.csv',
                               keep_default_na=False, na_values=['__'], encoding='utf-8')


def generate_dropdown():
    dframe = df_country_index
    lst = []
    for i in range(len(dframe)):
        lst.append({'label': dframe.iloc[i][0]+', '+dframe.iloc[i][1],
                    'value': dframe.iloc[i][1]})
    return dcc.Dropdown(
        id='country-dropdown',
        options=lst,
        placeholder="Select",
        clearable=False,
        searchable=True,
        value=dframe.iloc[-8][1],
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
    new_class = str(card_class).replace(' d-invisible', ' d-visible')
    return [new_class, dict_alpha_name[alpha]['name'], card_body_div]


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
                html.Span(className='label label-error', children=[
                    "Deceased:"
                ]),
                html.Span(className='label label-secondary', children=[
                    status[1]
                ])
            ]),
            html.Div(className='divider-vert'),
            html.Div(className='column col-3 col-mx-auto', children=[
                html.Span(className='label label-success', children=[
                    "Recovered:"
                ]),
                html.Span(className='label label-secondary', children=[
                    status[2]
                ])
            ]),
        ]),
        html.Div(className='divider'),
        html.Button(id='graph-btn-timeline', className='btn btn-primary', children=[
            'Show Timeline'
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


tabs_last = [0, 0, 0]


@app.callback(
    [Output('tab-cases', 'className'),
     Output('tab-deaths', 'className'),
     Output('tab-recovered', 'className'),
     Output('geomap-loader', 'children')],
    [Input('geo-cases', 'n_clicks'),
     Input('geo-deaths', 'n_clicks'),
     Input('geo-recovered', 'n_clicks')]
)
def geo_tabs_cases(c_btn, d_btn, r_btn):
    tab = 'tab-item'
    tab_active = 'tab-item active'
    tabs_cur = [int(c_btn), int(d_btn), int(r_btn)]
    global tabs_last
    clicked = [tabs_cur[i]-tabs_last[i] for i in range(3)]
    tabs_last = tabs_cur
    if clicked[0]:
        return tab_active, tab, tab, generate_geomap('cases')
    elif clicked[1]:
        return tab, tab_active, tab, generate_geomap('deaths')
    elif clicked[2]:
        return tab, tab, tab_active, generate_geomap('recovered')
    else:
        return tab, tab, tab, generate_geomap('cases')


def generate_geomap(status):
    fig = figure.fig_geo_map(status)
    return dcc.Graph(figure=fig, style={'width': '100%', 'height': '100%',
                                        'fontFamily': 'Roboto Mono', })
