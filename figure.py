import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def fig_line_chart(value, df_country, checklist):
    """Take pandas.dataframe - timeline of a country
    and generate line charts of total and daily
    by timeline.
    Arguments:
        value {str} -- [country's name]
        df_country {pandas.DataFrame} --  columns:'cases', 'recovered', 'deaths', 'last_update'
        checklist - ['infected', 'deaths', 'recovered']
    Returns:
        plotly.graph_objects.Figure -- Desired subplots
    """
    fig = go.Figure()
    df_country['newcases'] = df_country['cases'].diff(1)
    df_country['newrecovered'] = df_country['recovered'].diff(1)
    df_country['newdeaths'] = df_country['deaths'].diff(1)

    fig = make_subplots(rows=1, cols=2)
    fig = fig_filter_checklist(fig, df_country, checklist)

    # fig.update_traces(hoverinfo='x+y', stackgroup='one')
    fig.update_layout(hovermode='x', autosize=True,
                      title={
                          'text': "Confirmed Cases From Day One",
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'},
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
                      yaxis=dict(autorange=True, fixedrange=False),
                      #   xaxis_rangeslider_visible=True, xaxis_rangeslider_thickness=0.05,
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
    fig = (fig_add_dropdown(fig))
    return fig


def fig_filter_checklist(fig, df_country, checklist):
    if ('infected' in checklist):
        fig.add_trace(go.Scatter(x=df_country['last_update'],
                                 y=df_country['cases'],
                                 mode='lines',
                                 legendgroup='infected',
                                 name='Infected',
                                 line=dict(color='tomato')),
                      row=1, col=1
                      )
        fig.add_trace(go.Scatter(x=df_country['last_update'],
                                 y=df_country['newcases'],
                                 mode='lines',
                                 legendgroup='infected',
                                 name='Infected - Daily',
                                 line=dict(color='tomato', width=1.5),
                                 showlegend=True),
                      row=1, col=2,

                      )
    if 'recovered' in checklist:
        fig.add_trace(go.Scatter(x=df_country['last_update'],
                                 y=df_country['recovered'],
                                 mode='lines',
                                 legendgroup='recovered',
                                 name='Recovered',
                                 line=dict(color='forestgreen')),
                      row=1, col=1
                      )
        fig.add_trace(go.Scatter(x=df_country['last_update'],
                                 y=df_country['newrecovered'],
                                 mode='lines',
                                 legendgroup='recovered',
                                 name='Recovered - Daily',
                                 line=dict(color='forestgreen', width=1.5),
                                 showlegend=True),
                      row=1, col=2,
                      )
    if 'deaths' in checklist:
        fig.add_trace(go.Scatter(x=df_country['last_update'],
                                 y=df_country['deaths'],
                                 mode='lines',
                                 legendgroup='deceased',
                                 name='Deceased',
                                 line=dict(color='firebrick', width=1)),
                      row=1, col=1
                      )
        fig.add_trace(go.Scatter(x=df_country['last_update'],
                                 y=df_country['newdeaths'],
                                 mode='lines',
                                 legendgroup='deceased',
                                 name='Deceased - Daily',
                                 line=dict(color='firebrick', width=1.5),
                                 showlegend=True),
                      row=1, col=2,
                      )
    return fig


def fig_add_dropdown(fig):
    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                showactive=True,
                buttons=list([
                    dict(
                        args=["mode", "lines"],
                        label="Lines",
                        method="restyle"
                    ),
                    dict(
                        args=["mode", "markers"],
                        label="Dots",
                        method="restyle"
                    ),
                    dict(
                        args=["mode", "lines+markers"],
                        label="Lines+Dots",
                        method="restyle"
                    ),
                ]),
                pad={"r": 10, "t": 10},
                x=0,
                xanchor="left",
                y=1.5,
                yanchor="top"
            ),
        ]
    )

    return fig


def fig_geo_map(status):
    """Generate a world map based on given case status:
    'cases','deaths','recovered

    Arguments:
        status {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    df = pd.read_csv('./data_rebase/country_all_status.csv',
                     encoding='utf-8', keep_default_na=False, na_values=['__'])
    # df['text'] = df['name']+'<br>' +\
    # 'Infected: '+str(df['cases']) + '<br>' + 'Deaths: '+str(df['deaths']) + '<br>' +\
    # 'Recovered: '+str(df['recovered'])
    if (status == 'cases'):
        color_mode = 'sunset'
    elif(status == 'deaths'):
        color_mode = 'reds'
    else:
        color_mode = 'greens'
    fig = go.Figure(data=go.Choropleth(
        locations=df['alpha-3'],
        z=df[status],
        locationmode='ISO-3',
        colorscale=color_mode,
        # autocolorscale=True,
        colorbar_title="Confirmed Cases",
        # text=df['cases']
        # color_continuous_scale='Inferno'
    )
    )
    fig.update_layout(autosize=True,
                      geo=dict(
                          showframe=True,
                          projection_type='eckert4'
                      ),
                      margin=dict(t=15, b=5, l=5, r=5),
                      template='plotly',
                      font=dict(
                          family='Roboto Slab, serif',
                          size=14,
                          color="#000000"
                      ),
                      )
    fig.update_geos(
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="LightBlue",
        showrivers=False, rivercolor="LightBlue",
        showcountries=True
    )
    return fig
