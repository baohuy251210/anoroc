import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime
import dataprocess
'''
-----------------------
Data Frame (pandas) to htmlTable
'''

df = pd.read_csv('jhu_sorted.csv', encoding='cp1252')
df.columns = ['Country', 'Infected', 'New Infected', 'Total Deaths', 'New Deaths',
              'Total Recovered', 'New Recovered']


def generate_table(dataframe, max_rows=40):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ]),
    ])


# def generate_dropdown

'''
-----------------------
App.py layouts part
'''
# external_stylesheets = ['https://codepen.io/baohuy251210/pen/KKdGQep.css']
external_stylesheets = ['https://codepen.io/baohuy251210/pen/rNOqdKv.css']
# external_scripts = ['https://codepen.io/zavoloklom/pen/IGkDz.js']
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

'''
layout styling
'''
# colors = {
#     'background': '#fcfffa',
#     'text': '#4f504e'
# }

app.layout = html.Div(
    children=[
        html.H1(children='COVID-19 Monitor Dashboard',
                style={
                    'fontWeight': 900,
                    'font-family': 'Roboto',
                    'margin-bottom': '5px',
                    'margin-top': '12px'
                },
                ),
        html.H4(children="Updated Daily (" + datetime.today().strftime('%m-%d-%Y')+")",
                style={
                    'textAlign': 'center',
                    'margin-top': '5px',

        },
        ),
        generate_table(df),
        html.H6(["Data is sourced from ",
                 html.A('John Hopkins CSSE',
                        href='https://github.com/CSSEGISandData/COVID-19'),
                 html.Br(),
                 " through a free API from Kyle Redelinghuys ",
                 html.A('COVID19API', href='covid19api.com')
                 ],
                style={
                    'font-style': 'italic'

        }
        )

    ])

if __name__ == '__main__':
    app.run_server(debug=False)
