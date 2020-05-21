import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import datetime


def fig_line_chart(value, df_country):
    """Take pandas.dataframe - timeline of a country 
    and generate line charts of total and daily 
    by timeline.
    Arguments:
        value {str} -- [country's name]
        df_country {pandas.DataFrame} --  columns:'cases', 'recovered', 'deaths', 'last_update'
    Returns:
        plotly.graph_objects.Figure -- Desired subplots
    """
    fig = go.Figure()
    df_country['newcases'] = df_country['cases'].diff(-1)
    df_country['newrecovered'] = df_country['recovered'].diff(-1)
    df_country['newdeaths'] = df_country['deaths'].diff(-1)
    fig = make_subplots(rows=1, cols=2,
                        )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['cases'],
                             mode='lines',
                             legendgroup='infected',
                             name='Infected',
                             line=dict(color='tomato')),
                  row=1, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['recovered'],
                             mode='lines',
                             legendgroup='recovered',
                             name='Recovered',
                             line=dict(color='forestgreen')),
                  row=1, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['deaths'],
                             mode='lines',
                             legendgroup='deceased',
                             name='Deceased',
                             line=dict(color='firebrick', width=1)),
                  row=1, col=1
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['newcases'],
                             mode='lines',
                             legendgroup='infected',
                             name='Infected - Daily',
                             line=dict(color='tomato', width=1.5),
                             showlegend=False),
                  row=1, col=2,

                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['newrecovered'],
                             mode='lines',
                             legendgroup='recovered',
                             name='Recovered - Daily',
                             line=dict(color='forestgreen', width=1.5),
                             showlegend=False),
                  row=1, col=2,
                  )
    fig.add_trace(go.Scatter(x=df_country['last_update'],
                             y=df_country['newdeaths'],
                             mode='lines',
                             legendgroup='deceased',
                             name='Deceased - Daily',
                             line=dict(color='firebrick', width=1.5),
                             showlegend=False),
                  row=1, col=2,
                  )
    # fig.update_traces(hoverinfo='x+y', stackgroup='one')
    fig.update_layout(hovermode='x', autosize=True,
                      legend=dict(x=0.4, y=-0.7),
                      showlegend=True,
                      font=dict(
                          family='Roboto Slab, serif',
                          size=14,
                          color="#000000"
                      ),
                      legend_orientation='h',
                      xaxis_title='Timeline',
                      yaxis_title='Reported Counts',
                      xaxis_range=[datetime.datetime(2020, 4, 10),
                                   datetime.datetime(2020, 5, 20)],
                      yaxis=dict(autorange=True, fixedrange=False),
                      xaxis_rangeslider_visible=True, xaxis_rangeslider_thickness=0.05,
                      )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="7d", step="day",
                     stepmode="backward"),
                dict(count=21, label="3week", step="day",
                     stepmode="backward"),
                dict(count=1, label="1m", step="month",
                     stepmode="backward"),
                dict(count=3, label="3m", step="month",
                     stepmode="backward"),
                dict(step="all")
            ]),

        ))
    fig.update_yaxes(nticks=6)
    return fig
