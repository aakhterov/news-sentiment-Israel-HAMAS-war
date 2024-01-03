from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from explanation import EXPLANATION

def get_title_container():
    """
    TODO
    :return:
    """
    return html.Div(
        id="title-container",
        children=[
            html.H1(children="News sentiment regarding the Israel-HAMAS war",
                    className="text-center, mt-4"),
            html.Hr(),
            dbc.Alert(children=[
                html.Span("Site has been created for studying purposes. All results are experimental by nature. "
                          "An AI model is still improving. "),
                dbc.Button("Show more...", id="collapse-link", color="link", n_clicks=0)
            ], color="warning", className="text-center"),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(EXPLANATION)),
                id="collapse",
                is_open=False,
                className="mb-3"
            ),
        ],
        style={"text-align": "center"}
    )


def get_controller_container(start_date, end_date, min_date, news_providers):
    """
    TODO
    :param start_date:
    :param end_date:
    :return:
    """
    return dbc.Row(
        id="controller-container",
        children=[
            dbc.Col(
                html.Div(
                    id="date-picker-container",
                    children=[
                        html.Div("Select date"),
                        dcc.DatePickerRange(
                            id="date-picker-select",
                            start_date=start_date,
                            end_date=end_date,
                            min_date_allowed=min_date,
                            max_date_allowed=end_date,
                            display_format="D/M/YYYY"
                        )
                    ]
                )
            ),
            dbc.Col(
                html.Div(
                    id="news-provider-container",
                    children=[
                        html.Div("News provider"),
                        dcc.Dropdown(news_providers, value=news_providers[0], id='news-provider-select'),
                    ]
                )
            )
        ],
        className="dbc"
    )


def get_back_button_container():
    """
    TODO
    :return:
    """
    return html.Div(
        id="back-button-container",
        children=[
            dbc.Button('Back', id="back-button", n_clicks=0, className="me-1")
        ],
        style = {'display': 'none'}
    )


def get_graph_container():
    """
    TODO
    :return:
    """
    return html.Div(
        id="graph-container",
        children= [
            dcc.Graph(id="sentiment-graph", figure={})
        ],
        className="dbc"
    )


def get_datatable_container():
    """
    TODO
    :return:
    """
    return dbc.Row ([
        dbc.Col(html.Div(), xs=0, sm=1, md=3, lg=3, xl=3),
        dbc.Col([
            html.Div(
                id="total-stat-container",
                children=[
                    html.H3('Total sentiment'),
                    html.Div(
                        id="total-news-datatable-container",
                        children=dash_table.DataTable(id="total-news-datatable"),
                        className="dbc my-4"
                    )
                ]
            ),
            html.H3(id="details-sentiment-title", children='Sentiment by days'),
            html.Div(
                id="news-datatable-container",
                children=dash_table.DataTable(id="news-datatable"),
                className="dbc my-4"
            )
        ],
            xs=12, sm=10, md=6, lg=6, xl=6
        ),
        dbc.Col(html.Div(), xs=0, sm=1, md=3, lg=3, xl=3),
    ])


def get_modal():
    return dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Header", id="modal-title")),
                    dbc.ModalBody(id="modal-body"),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal",
                size="lg",
                is_open=False,
            )

