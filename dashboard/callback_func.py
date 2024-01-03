from datetime import datetime, timedelta
from dash import Dash, html, dash_table, dcc, callback, Input, Output
import plotly.express as px

from sentiment import get_sentiment_distribution_per_day

@callback(
    Output(component_id="news-datatable-container", component_property="children"),
    [
        Input(component_id="date-picker-select", component_property="start_date"),
        Input(component_id="date-picker-select", component_property="end_date")
    ]
)
def update_table(start_date, end_date):
    """
    TODO
    :param start_date:
    :param end_date:
    :return:
    """
    filtered_df = df[(df['datetime'] >= start_date) &
                     (df['datetime'] < datetime.strptime(end_date, "%Y-%m-%d") +
                      timedelta(days=1))]
    modified_df = get_sentiment_distribution_per_day(filtered_df, 0.5).reset_index()
    modified_df['datetime'] = modified_df['datetime'].apply(lambda x: x.strftime("%d-%m-%Y"))

    return [dash_table.DataTable(id="news-datatable",
                                 data=modified_df.to_dict('records'),
                                 page_size=20)]