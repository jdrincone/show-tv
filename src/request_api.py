import requests
import pandas as pd
import datetime
import json
import fastparquet
import ydata_profiling
from ydata_profiling.utils.cache import cache_file
import logging
from metadata.paths import Paths


def list_dates(start_date, end_date) -> list:
    """

    :param start_date:
    :param end_date:
    :return:
    """
    dates = []
    for day in range((end_date - start_date).days + 1):
        dates.append((start_date + datetime.timedelta(days=day)).strftime('%Y-%m-%d'))

    return dates


def json_api(url: str) -> json:
    """
    Args:
        url:
    """

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def save_json(data, name_file):

    with open(name_file, "w") as file:
        json.dump(data, file)


def transform_json_to_dataframe(data: json) -> tuple:
    """
    Args:
        data:

    Return:
    """
    df = pd.DataFrame(data)

    list_df = []
    for element in data:
        detalle = element.get('_embedded')
        df_detalle = pd.DataFrame.from_dict(detalle, orient='index')
        list_df.append(df_detalle)
    detalle_df = pd.concat(list_df)

    return df, detalle_df


def save_parquet(df, name_parquet):
    fastparquet.write(name_parquet, df, compression='SNAPPY')


def save_profile(df, name_profile):
    profile_report = df.profile_report(html={"style": {"full_width": True}})

    path_profile = path.root_profiling(name_profile)
    profile_report.to_file(path_profile)


if __name__ == '__main__':
    start_date = datetime.date(2022, 12, 1)
    end_date = datetime.date(2022, 12, 31)

    dates = list_dates(start_date, end_date)
    for dia in dates:
        url = f"http://api.tvmaze.com/schedule/web?date={dia}"
        data = json_api(url)

        path = Paths()
        name_json = path.root_json(dia)
        save_json(data, name_json)

        df, detalle_df = transform_json_to_dataframe(data)

        name_parquet_df = path.root_parquet(f"show_{dia}")
        name_parquet_detalle_df = path.root_parquet(f"show_detalle_{dia}")
        save_parquet(df, name_parquet_df)
        save_parquet(df, name_parquet_detalle_df)

        name_profile_df = path.root_profiling(f'show_{dia}')
        save_profile(df, name_profile_df)

        name_profile_det_df = path.root_profiling(f'show_detalle_{dia}')
        save_profile(detalle_df, name_profile_det_df)


        print("Informe de perfil generado y guardado en perfil_df.html")






