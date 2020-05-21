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

from app import app
database_local_status = False
df_country_index = database.get_df_country_index(database_local_status)


@app.callback(
    Output('dropdown-output', 'children'),
    [Input('country-dropdown', 'value')])
def update_output_sql(value):
    """Input- value: country's alpha
    Arguments:
        value {[type]} -- [description]
    """
    country_name = database.get_country_from_alpha(
        value, database_local_status)[1]

    df_selected_country = database.get_country_status(
        value, database_local_status).drop(columns='alpha2')
    df_selected_country['name'] = df_selected_country['name'].apply(
        lambda x: country_name)
    df_selected_country = df_selected_country.rename(columns={"name": "Country", "cases": "Infected", 'deaths': 'Deaths', 'recovered': 'Recovered',
                                                              'last_update': 'Last Update GMT+0'})

    fig = figure.fig_line_chart(
        country_name, database.get_country_timeline(value))
    return html.Div([dash_table.DataTable(
        id='selected',
        columns=[{'name': i, 'id': i} for i in df_selected_country.columns],
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
        data=df_selected_country.to_dict('records')
    ),
        dcc.Graph(figure=fig, style={'marginTop': '25px', 'width': '100%'})
    ]
    )


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


def generate_dropdown(dframe):
    lst = []
    for i in range(len(dframe)):
        lst.append({'label': dframe.iloc[i][1]+', '+dframe.iloc[i][0],
                    'value': dframe.iloc[i][0]})

    # print(lst)
    return dcc.Dropdown(
        id='country-dropdown',
        options=lst,
        placeholder="Select country to inspect",
        clearable=False,
        searchable=True,
        value=dframe.iloc[-8][0],  # value = 'us'
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
