import pandas as pd


def get_class(pos_score, thr):
    """
    TODO
    :param pos_score:
    :param thr:
    :return:
    """
    if pos_score - (1 - pos_score) >= thr:
        return 1
    elif (1 - pos_score) - pos_score >= thr:
        return -1
    else:
        return 0


def get_classes(df, thr):
    """

    :param df:
    :param thr:
    :return:
    """
    data = {"datetime": df['datetime'],
            "class": df['pro_israel_score'].apply(lambda x: get_class(x, thr))}
    df = pd.DataFrame(data)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df


def get_sentiment_distribution(df_with_classes: pd.DataFrame, freq='D'):
    """
    TODO
    :param df_with_classes:
    :param freq:
    :return:
    """
    df = df_with_classes.set_index('datetime')
    negative_df = df[df["class"] == -1].groupby(pd.Grouper(freq=freq)).count().rename(columns={"class": "anti-Israel"})
    neutral_df = df[df["class"] == 0].groupby(pd.Grouper(freq=freq)).count().rename(columns={"class": "neutral"})
    positive_df = df[df["class"] == 1].groupby(pd.Grouper(freq=freq)).count().rename(columns={"class": "pro-Israel"})

    result = pd.concat([negative_df, neutral_df, positive_df], axis=1).fillna(0).astype('int')

    total_news_per_day = result["anti-Israel"] + result["neutral"] + result["pro-Israel"]
    total_news_per_day.replace(0, 1e-10, inplace=True)
    result["anti-Israel_proc"] = result["anti-Israel"]/total_news_per_day
    result["neutral_proc"] = result["neutral"]/total_news_per_day
    result["pro-Israel_proc"] = result["pro-Israel"]/total_news_per_day

    return result


def get_total_statistic(df: pd.DataFrame()) -> pd.DataFrame:
    """
    TODO
    :param df:
    :return:
    """
    total = df[["anti-Israel", "neutral", "pro-Israel"]].sum().sum()
    anti_total = df["anti-Israel"].sum()
    neutral_total = df["neutral"].sum()
    pro_total = df["pro-Israel"].sum()
    min_date = df['datetime'].min()
    max_date = df['datetime'].max()

    data = {"datetime": min_date.strftime("%d/%m") + " - " + max_date.strftime("%d/%m"),
            "anti-Israel": f"{anti_total} ({anti_total/total:.1%})",
            "neutral": f"{neutral_total} ({neutral_total/total:.1%})",
            "pro-Israel": f"{pro_total} ({pro_total/total:.1%})"}

    return pd.DataFrame([data])