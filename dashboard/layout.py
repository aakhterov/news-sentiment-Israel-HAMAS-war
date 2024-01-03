from datetime import datetime, timedelta

import pandas as pd
from dash import html, dash_table, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

from maindash import appplication, TEMPLATE_NAME
from database import (get_dataframe_from_db, get_start_date, get_end_date, get_news_provider,
                      get_min_date)
from sentiment import get_class, get_classes, get_sentiment_distribution, get_total_statistic
from html_container import (get_datatable_container, get_controller_container,
                            get_graph_container, get_back_button_container,
                            get_title_container, get_modal
                            )


THRESHOLD = 0.5
PRO_ISRAEL_COLOR = "#4bbf73"
NEUTRAL_COLOR = "#f0ad4e"
ANTI_ISRAEL_COLOR = "#d9534f"

df = pd.DataFrame()
df_with_classes = pd.DataFrame()
start_date = None
end_date = None
news_providers = None


def make_layout():
    """
    TODO
    :return:
    """
    global df, df_with_classes, start_date, end_date, news_providers
    df = get_dataframe_from_db()
    df_with_classes = get_classes(df, THRESHOLD)
    start_date = get_start_date(df)
    end_date = get_end_date(df)
    min_date = get_min_date(df)
    news_providers = get_news_provider(df)

    controller_container = get_controller_container(start_date, end_date, min_date, news_providers)
    back_button_container = get_back_button_container()
    graph_container = get_graph_container()
    table_container = get_datatable_container()
    modal = get_modal()

    return dbc.Row ([
        dbc.Col(html.Div(), xs=0, sm=1, md=1, lg=1, xl=1),
        dbc.Col(
            html.Div(
                id="main-container",
                children=[
                    get_title_container(),
                    controller_container,
                    back_button_container,
                    graph_container,
                    table_container,
                    dcc.Input(id="is_intraday", type="hidden", value=0),
                    modal,
                    dcc.Store(id='memory')
                ]
            ),
            xs=12, sm=10, md=10, lg=10, xl=10
        ),
        dbc.Col(html.Div(), xs=0, sm=1, md=1, lg=1, xl=1),
    ])


def get_daily_figure(df: pd.DataFrame):
    """
    TODO
    :param df:
    :return:
    """
    hovertext = [f"<b>{row['datetime']}</b><br>"
                 f"pro-Israel news: {row['pro-Israel']} ({row['pro-Israel_proc']:.0%})<br>"
                 f"neutral news: {row['neutral']} ({row['neutral_proc']:.0%})<br>"
                 f"anti-Israel news: {row['anti-Israel']} ({row['anti-Israel_proc']:.0%})"
                 for _, row in df.iterrows()]

    anti_israel_bars = go.Bar(x=df['datetime'],
                              y=df['anti-Israel'],
                              name='anti-Israel news',
                              marker={"color": ANTI_ISRAEL_COLOR},
                              text=[f"{y}({z:.0%})" for y, z in zip(df['anti-Israel'],
                                                                    df['anti-Israel_proc'])],
                              textfont={"color": "rgb(0, 0, 0)", "size": 14},
                              textposition='auto',
                              hoverinfo="text",
                              hoverlabel={"bgcolor": "rgb(255,255,255)"},
                              hovertext=hovertext)
    neutral_bars = go.Bar(x=df['datetime'],
                          y=df['neutral'],
                          name='neutral news',
                          marker={"color": NEUTRAL_COLOR},
                          text=[f"{y}({z:.0%})" for y, z in zip(df['neutral'],
                                                                df['neutral_proc'])],
                          textfont={"color": "rgb(0, 0, 0)", "size": 14},
                          textposition='auto',
                          hoverinfo="text",
                          hoverlabel={"bgcolor": "rgb(255,255,255)"},
                          hovertext=hovertext)
    pro_israel_bars = go.Bar(x=df['datetime'],
                             y=df['pro-Israel'],
                             name='pro-Israel news',
                             marker={"color": PRO_ISRAEL_COLOR},
                             text=[f"{y}({z:.0%})" for y, z in zip(df['pro-Israel'],
                                                                   df['pro-Israel_proc'])],
                             textfont={"color": "rgb(0, 0, 0)", "size": 14},
                             textposition='auto',
                             hoverinfo="text",
                             hoverlabel={"bgcolor": "rgb(255,255,255)"},
                             hovertext=hovertext)

    fig = go.Figure()
    fig.add_trace(anti_israel_bars)
    fig.add_trace(neutral_bars)
    fig.add_trace(pro_israel_bars)

    fig.update_layout(
        xaxis_tickfont_size=14,
        xaxis_tickangle=-45,
        yaxis=dict(
            title='News count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        # barmode='group',
        barmode='stack',
        bargap=0.25,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
    )

    return fig


def get_hourly_figure(df: pd.DataFrame):
    """
    TODO
    :param df:
    :return:
    """
    hovertext = [f"<b>{row['datetime']}</b><br>"
                 f"pro-Israel news: {row['pro-Israel']}<br>"
                 f"neutral news: {row['neutral']}<br>"
                 f"anti-Israel news: {row['anti-Israel']}"
                 for _, row in df.iterrows()]

    anti_israel_bars = go.Bar(x=df['datetime'],
                              y=df['anti-Israel'],
                              name='anti-Israel news',
                              # textposition='auto',
                              marker={"color": ANTI_ISRAEL_COLOR},
                              # text=df['anti-Israel'],
                              # textfont={"color": "rgb(0, 0, 0)"},
                              hoverinfo="text",
                              hoverlabel={"bgcolor": "rgb(255,255,255)"},
                              hovertext=hovertext)
    neutral_bars = go.Bar(x=df['datetime'],
                          y=df['neutral'],
                          name='neutral news',
                          marker={"color": NEUTRAL_COLOR},
                          # text=df['neutral'],
                          # textfont={"color": "rgb(0, 0, 0)"},
                          hoverinfo="text",
                          hoverlabel={"bgcolor": "rgb(255,255,255)"},
                          hovertext=hovertext)
    pro_israel_bars = go.Bar(x=df['datetime'],
                             y=df['pro-Israel'],
                             name='pro-Israel news',
                             marker={"color": PRO_ISRAEL_COLOR},
                             # text=df['pro-Israel'],
                             # textfont={"color": "rgb(0, 0, 0)"},
                             hoverinfo="text",
                             hoverlabel={"bgcolor": "rgb(255,255,255)"},
                             hovertext=hovertext)

    fig = go.Figure()
    fig.add_trace(anti_israel_bars)
    fig.add_trace(neutral_bars)
    fig.add_trace(pro_israel_bars)

    fig.update_layout(
        xaxis_tickfont_size=14,
        xaxis_tickangle=-45,
        yaxis=dict(
            title='News count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        # barmode='group',
        barmode='stack',
        bargap=0.25,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
    )

    return fig


@appplication.callback(
    Output(component_id="total-news-datatable-container", component_property="children"),
    Output(component_id="news-datatable-container", component_property="children"),
    Output(component_id="sentiment-graph", component_property="figure"),
    [
        Input(component_id="date-picker-select", component_property="start_date"),
        Input(component_id="date-picker-select", component_property="end_date"),
        Input(component_id="back-button", component_property="n_clicks")
    ]
)
def update_graph_and_table(start_date, end_date, n_clicks):
    """
    TODO
    :param start_date:
    :param end_date:
    :param n_clicks:
    :return:
    """
    filtered_df = df_with_classes[(df_with_classes['datetime'] >= start_date) &
                                  (df_with_classes['datetime'] < datetime.strptime(end_date, "%Y-%m-%d") +
                                   timedelta(days=1))]
    modified_df = get_sentiment_distribution(filtered_df, 'D').reset_index()

    total_df = get_total_statistic(modified_df)

    modified_df['datetime'] = modified_df['datetime'].apply(lambda x: x.strftime("%d-%m-%Y"))
    fig = get_daily_figure(modified_df)

    total_datatable = dash_table.DataTable(id="total-news-datatable",
                                     data=total_df.to_dict('records'),
                                     columns=[{"id": "datetime", "name": "Date interval"},
                                              {"id": "anti-Israel", "name": "anti-Israel news"},
                                              {"id": "neutral", "name": "Neutral news"},
                                              {"id": "pro-Israel", "name": "pro-Israel news"}],
                                     style_as_list_view=True,
                                     style_cell={'padding': '5px'},
                                     style_header={
                                         'backgroundColor': 'rgb(210, 210, 210)',
                                         'color': 'black',
                                         'fontWeight': 'bold'
                                     },
                                     style_data={
                                         'color': 'black',
                                         'backgroundColor': 'white'
                                     },
                                     style_cell_conditional=[
                                         {
                                             'if': {'column_id': "datetime"},
                                             'textAlign': 'left'
                                         }
                                     ])

    modified_df["anti-Israel"] = modified_df["anti-Israel"].astype(str) + \
                                 " (" + round(modified_df["anti-Israel_proc"]*100, 1).astype(str) + "%)"
    modified_df["neutral"] = modified_df["neutral"].astype(str) + \
                              " (" + round(modified_df["neutral_proc"]*100, 1).astype(str) + "%)"
    modified_df["pro-Israel"] = modified_df["pro-Israel"].astype(str) + \
                                " (" + round(modified_df["pro-Israel_proc"]*100, 1).astype(str) + "%)"
    datatable = dash_table.DataTable(id="news-datatable",
                                     data=modified_df.to_dict('records'),
                                     columns=[{"id": "datetime", "name": "Date"},
                                              {"id": "anti-Israel", "name": "anti-Israel news"},
                                              {"id": "neutral", "name": "Neutral news"},
                                              {"id": "pro-Israel", "name": "pro-Israel news"}],
                                     style_as_list_view=True,
                                     style_cell={'padding': '5px'},
                                     style_header={
                                         'backgroundColor': 'rgb(210, 210, 210)',
                                         'color': 'black',
                                         'fontWeight': 'bold'
                                     },
                                     style_data={
                                         'color': 'black',
                                         'backgroundColor': 'white'
                                     },
                                     style_data_conditional=[
                                         {
                                             'if': {'row_index': 'odd'},
                                             'backgroundColor': 'rgb(220, 220, 220)',
                                         }
                                     ],
                                     style_cell_conditional=[
                                         {
                                             'if': {'column_id': "datetime"},
                                             'textAlign': 'left'
                                         }
                                     ],
                                     page_size=20)

    return total_datatable, datatable, fig


@appplication.callback(
    Output("news-datatable-container", "children", allow_duplicate=True),
    Output("details-sentiment-title", "children", allow_duplicate=True),
    Output("total-stat-container", "style", allow_duplicate=True),
    Output('sentiment-graph', 'figure', allow_duplicate=True),
    Output('back-button-container', 'style', allow_duplicate=True),
    Output('controller-container', 'style', allow_duplicate=True),
    Output('is_intraday', 'value', allow_duplicate=True),
    Output('memory', 'data'),
    [
        Input('sentiment-graph', 'clickData'),
        # Input('news-datatable', 'active_cell'),
        State('is_intraday', 'value'),
    ], prevent_initial_call=True
)
def press_on_graph(clickData, value):
    """
    TODO
    :param clickData:
    :param value:
    :return:
    """
    if value or clickData is None:
        raise PreventUpdate

    selected_day = datetime.strptime( clickData['points'][0]['x'], "%d-%m-%Y")

    filtered_df = df_with_classes[(df_with_classes['datetime'] >= selected_day) &
                                  (df_with_classes['datetime'] < selected_day + timedelta(days=1))]
    modified_df = get_sentiment_distribution(filtered_df, 'H').reset_index()
    modified_df['datetime'] = modified_df['datetime'].apply(lambda x: x.strftime("%H:%M"))
    fig = get_hourly_figure(modified_df)

    filtered_df = df[(df['datetime'] >= selected_day) &
                     (df['datetime'] < selected_day + timedelta(days=1))]
    filtered_df["class"] = filtered_df['pro_israel_score'].apply(lambda x: get_class(x, THRESHOLD))
    filtered_df = (filtered_df.loc[:, ['url', 'datetime', 'title', 'news_text', 'class']]
                   .sort_values(by=["datetime"])
                   .reset_index(drop=True))
    filtered_df["datetime"] = filtered_df["datetime"].apply(lambda x: x.strftime("%H:%M"))
    filtered_df["url"] = filtered_df["url"].apply(lambda x: f"[Link]({x})")
    filtered_df.reset_index(drop=False, inplace=True)
    filtered_df['index'] += 1
    # filtered_df["sentiment"] = ["" for _ in range(len(filtered_df))]
    datatable = dash_table.DataTable(id="news-datatable",
                                     data=filtered_df.to_dict('records'),
                                     columns=[{'name': '#', 'id': 'index'},
                                              {'name': 'Time', 'id': 'datetime'},
                                              {'name': 'News title', 'id': 'title'},
                                              {'name': 'URL', 'id': 'url', 'presentation': 'markdown'}],
                                     page_size=20,
                                     # tooltip_duration=None,
                                     # tooltip_data=[{
                                     #     'title': {'value': row['news_text'],
                                     #               'type': 'markdown'}
                                     # } for row in filtered_df.to_dict('records')],
                                     css=[{
                                         'selector': '.dash-table-tooltip',
                                         'rule': 'background-color: white !important;'
                                                 'font-family: monospace; '
                                                 'color: rgb(0, 0, 0) !important;'
                                                 'width:700px !important;'
                                                 'max-width: 700px !important;'
                                                 'min-width: 300px !important;'
                                     }],
                                     style_as_list_view=True,
                                     style_cell={'padding': '5px'},
                                     style_header={
                                         'backgroundColor': 'rgb(210, 210, 210)',
                                         'color': 'black',
                                         'fontWeight': 'bold'
                                     },
                                     style_data={
                                         'color': 'black',
                                         'backgroundColor': 'white'
                                     },
                                     style_data_conditional=[
                                         {
                                             'if': {'row_index': 'odd'},
                                             'backgroundColor': 'rgb(220, 220, 220)',
                                         },
                                         {
                                             'if': {'filter_query': '{class} = 1', 'column_id': 'index'},
                                             'backgroundColor': PRO_ISRAEL_COLOR,
                                             'color': 'white'
                                         },
                                         {
                                             'if': {'filter_query': '{class} = 0', 'column_id': 'index'},
                                             'backgroundColor': NEUTRAL_COLOR,
                                             'color': 'white'
                                         },
                                         {
                                             'if': {'filter_query': '{class} = -1', 'column_id': 'index'},
                                             'backgroundColor': ANTI_ISRAEL_COLOR,
                                             'color': 'white'
                                         },
                                     ],
                                     style_cell_conditional=[
                                         {
                                             'if': {'column_id': "datetime"},
                                             'textAlign': 'left'
                                         },
                                         {
                                             'if': {'column_id': "title"},
                                             'textAlign': 'left'
                                         }
                                     ],
                                     )

    total_stat_style = {'display': 'none'}
    details_title = "Sentiment by hours"
    back_button_style = {'display': 'block'}
    controller_style = {'display': 'none'}
    is_intraday = 1

    return (datatable, details_title, total_stat_style, fig,
            back_button_style, controller_style, is_intraday, filtered_df.to_dict('records'))


@appplication.callback(
    Output('back-button-container', 'style', allow_duplicate=True),
    Output('controller-container', 'style', allow_duplicate=True),
    Output("details-sentiment-title", "children", allow_duplicate=True),
    Output("total-stat-container", "style", allow_duplicate=True),
    Output('is_intraday', 'value', allow_duplicate=True),
    Input('back-button', 'n_clicks'), prevent_initial_call=True)
def press_back_button(n_clicks):
    """
    TODO
    :param n_clicks:
    :return:
    """
    back_button_style = {'display': 'none'}
    controller_style = {}
    total_stat_style = {}
    details_title = "Sentiment by days"
    is_intraday = 0

    return back_button_style, controller_style, details_title, total_stat_style, is_intraday


@appplication.callback(
    Output('modal-title', 'children'),
    Output('modal-body', 'children'),
    Output("modal", "is_open"),
    [
        Input("news-datatable", "active_cell"),
        Input('memory', 'data'),
    ],
    [
        State('is_intraday', 'value'),
        State('news-datatable', 'page_current'),
        State('news-datatable', 'page_size'),
        State("modal", "is_open")
    ], prevent_initial_call=True
)
def display_news_text(click_data, data, value, page_current, page_size, is_open):
    if click_data is None or value != 1:
        raise PreventUpdate

    page_current = page_current if page_current is not None else 0
    record_number = page_current * page_size + click_data["row"]

    # text = f'{data[record_number]["news_text"]}\n\n<a href={data[record_number]["url"]}>{data[record_number]["url"]}</a>'

    return data[record_number]["title"], data[record_number]["news_text"], True


@appplication.callback(
    Output("modal", "is_open", allow_duplicate=True),
    Input("close", "n_clicks"), prevent_initial_call=True
)
def toggle_modal(n_clicks):
    if n_clicks:
        return False
    return True


@appplication.callback(
    Output("collapse", "is_open"),
    [Input("collapse-link", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
