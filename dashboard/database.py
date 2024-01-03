import os
from typing import List
from datetime import datetime, timedelta
import pandas as pd

SHOW_AMOUNT_OF_DAYS_AT_START = 14

def get_database_url(db_host, db_user, db_pass):
    """
    TODO
    :param db_host:
    :param db_user:
    :param db_pass:
    :return:
    """
    return f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:5432/news"


def get_dataframe_from_db() -> pd.DataFrame:
    """
    TODO
    :return:
    """
    database_url = get_database_url(db_host=os.environ["DB_HOSTNAME"],
                                    db_user=os.environ["DB_USER"],
                                    db_pass=os.environ["DB_USER_PASSWORD"])

    df = pd.read_sql_table('news', database_url, index_col='id', parse_dates=['datetime'])
    return df


def get_min_date(df: pd.DataFrame) -> datetime:
    """
    TODO
    :param df:
    :return:
    """
    return df['datetime'].min().date()


def get_start_date(df: pd.DataFrame) -> datetime:
    """
    TODO
    :param df:
    :return:
    """
    return get_end_date(df) - timedelta(days=SHOW_AMOUNT_OF_DAYS_AT_START)


def get_end_date(df: pd.DataFrame) -> datetime:
    """
    TODO
    :param df:
    :return:
    """
    return df['datetime'].max().date()


def get_news_provider(df: pd.DataFrame) -> List:
    """
    TODO
    :param df:
    :return:
    """
    return list(set((df["provider"] + " (" + df["source"] + ")")))