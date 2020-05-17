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
Data Frame (pandas) to htmlTable
'''

df = pd.read_csv('jhu_sorted.csv', encoding='cp1252')
df.columns = ['Country', 'Infected', 'New Infected', 'Total Deaths', 'New Deaths',
              'Total Recovered', 'New Recovered']
df_search = pd.read_csv('jhu.csv', encoding='cp1252')
df_search_name_index = pd.read_csv(
    'jhu.csv', index_col='Country', encoding='cp1252')
df_search.columns = ['Country', 'Infected', 'New Infected', 'Total Deaths', 'New Deaths',
                     'Total Recovered', 'New Recovered']


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
            'font-family': 'Jost',
            'display': 'inline-block',
            'text-align': 'center',
            'font-style': 'bold',
            'margin': '0 auto',
            'color': 'rgba(0,0,0,0.6)',
            'width': '40%',
            'position': 'relative',
            'vertical-align': 'middle',
            'font-family': 'Roboto',
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
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(len(dataframe))
            ]),
        ], style={
            'margin-top': '3px',
            'color': 'rgba(0,0,0,0.87)'
        })


# def generate_dropdown

"""
-----------------------
App.py layouts part
"""
# external_stylesheets = ['https://codepen.io/baohuy251210/pen/KKdGQep.css']
external_stylesheets = [
    'https://codepen.io/baohuy251210/pen/rNOqdKv.css']
# external_scripts = ['https://codepen.io/zavoloklom/pen/IGkDz.js']
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    children=[

        html.H1(children='ANOROC - Covid19 Monitor',
                style={
                    'margin-bottom': '5px',
                    'margin-top': '12px',
                    'vertical-align': 'center',
                    'text-align': 'center'
                },
                ),
        html.H4(children="Updated Daily (" + datetime.today().strftime('%m-%d-%Y')+")",
                style={
            'textAlign': 'center',
            'margin-top': '5px',

        },
        ),
        html.Br(),
        html.H5('Select Country to Inspect:', style={
            'text-align': 'center',
        }),
        generate_dropdown(df_search),
        html.Div(id='dropdown-output',
                 style={
                     'font-family': 'Roboto',
                     'width': '75%',
                     'text-align': 'center',
                     'vertical-align': 'center',
                     'display': 'inline-block'
                 }),
        html.H5('Collected Data:', style={
            'margin-bot': '0px',
            'margin-top': '12px',
            'text-align': 'center',
        }),
        generate_table(df),
        html.H6(["Data is sourced from ",
                 html.A('John Hopkins CSSE',
                        href='https://github.com/CSSEGISandData/COVID-19'),
                 html.Br(),
                 " through a free API from Kyle Redelinghuys ",
                 html.A('COVID19API', href='covid19api.com')
                 ],
                style={
            'font-style': 'italic',

        }
        )
    ], style={
        'overflow': 'hidden'
    })


@app.callback(
    Output('dropdown-output', 'children'),
    [Input('country-dropdown', 'value')])
def update_output(value):
    newdf = df_search[df_search['Country'] == value]

    return dash_table.DataTable(
        id='selected',
        columns=[{'name': i, 'id': i} for i in newdf.columns],
        style_cell={
            'whitespace': 'normal',
            'minWidth': '130px', 'width': '130px', 'maxWidth': '130px',
            'fontSize': 15,
            'text-align': 'center',
            'color': 'rgba(0,0,0,0.87)',
            'font-family': 'Jost'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Country'},
             'width': '23%'},
            {'if': {'column_id': 'Infected'},
             'width': '10%'},

        ],
        data=newdf.to_dict('records')
    )


if __name__ == '__main__':
    app.run_server(debug=True)
