import requests
import pandas as pd
import datetime
import json
import fastparquet
import itertools
import logging
import ydata_profiling

from ydata_profiling.utils.cache import cache_file

from metadata.paths import Paths


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


path = Paths()


def list_dates(start_date: datetime.date, end_date: datetime.date) -> list:
    """ Lista con las fechas entre dos fechas de interés.

    Args:
    start_date: Fecha inicial
    end_date: Fecha final

    Return
        listado con fechas de interés.
    """
    dates = []
    for day in range((end_date - start_date).days + 1):
        dates.append((start_date + datetime.timedelta(days=day)).strftime('%Y-%m-%d'))

    return dates


def json_api(url: str) -> json:
    """ Request a url.
    Args:
        url: url de trabajo.

    Return
        json con indormación solicitada.
    """

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def save_json(data: json, name_file: str):
    """Almacena información en formato json.
    Args:
        data: Datos de trabajo.
        name_file: nombre para el json.
    """

    with open(name_file, "w") as file:
        json.dump(data, file)


def transform_json_to_dataframe(data: json) -> tuple:
    """ Transforma información de un json a un conjunto de dataframe.
    Args:
        data: json con data a transformar.

    Return:
        conjunto de Dataframe contenidos en una tupla.
    """
    df = pd.DataFrame(data)

    list_df = []
    for element in data:
        detalle = element.get('_embedded')
        df_detalle = pd.DataFrame.from_dict(detalle, orient='index')
        df_detalle.rename(columns={'id': 'id_embedded'}, inplace=True)

        df_detalle['id'] = element.get('id')
        list_df.append(df_detalle)
    detalle_df = pd.concat(list_df)
    df = dataclean_to_dataframe(df)

    return df, detalle_df


def save_parquet(df: pd.DataFrame, name_parquet: str):
    """Almacena dataframe en formato parquet con compressión snappy.
    Args:
        df: Datos de trabajo.
        name_parquet: nombre para el parquet.
    """
    fastparquet.write(name_parquet, df, compression='SNAPPY')


def save_profile(df: pd.DataFrame, name_profile: str):
    """Almacena profile de un dataframe.
    Args:
        df: Datos de trabajo.
        name_profile: nombre para el profile.
        """
    profile_report = df.profile_report(html={"style": {"full_width": True}})
    profile_report.to_file(name_profile)


def dataclean_to_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """ Depuración y ordenamientos de las categorias que pueden tomar algunas fetures en
    el dataframe de trabajo.

    Args:
        data: Datos de trabajo.

    Return
        Dataframe depurado.
    """
    data['rating_average'] = data.rating.apply(lambda x: x.get('rating'))
    data['medium'] = data.image.apply(lambda x: x.get('medium') if x is not None else None)
    data['original'] = data.image.apply(lambda x: x.get('original') if x is not None else None)
    data['_links_self'] = data['_links'].apply(lambda x: x.get('self').get('href') if x is not None else None)
    data['_links_show'] = data['_links'].apply(lambda x: x.get('show').get('href') if x is not None else None)
    data['id_embedded'] = data['_embedded'].apply(lambda x: x.get('show').get('id'))

    cols = ['id', 'id_embedded', 'url', 'name', 'season', 'number', 'type',
            'airdate', 'airtime', 'airstamp', 'runtime', 'rating_average',
            'medium', 'original', '_links_self', '_links_show', 'summary']
    data_dep = data.loc[:, cols]
    return data_dep


def conteo_show_tv_por_genero(detalle_data: pd.DataFrame) -> pd.DataFrame:
    """ Conteo de la cantidad de show por género. Existen show que pertenecen a varios generos,
    en este caso se cuenta en mismo show para todos los generos posibles al cual pertenece.

    Args:
        detalle_data: Show emítidos en Dicciembre del 2022.

    Return
        Cantidad de show de tv segmentado por género.
    """
    genero_show = detalle_data.genres.tolist()
    generos = pd.DataFrame({'genero': itertools.chain(*genero_show)})
    show_genero = pd.DataFrame(generos.genero.value_counts())
    show_genero.columns = ['cantidad_show']
    show_genero.reset_index(inplace=True)

    return show_genero


def lista_dominios_oficiales_show_tv(detalle_data: pd.DataFrame) -> list:
    """ Lista los dominios oficiales

    Args:
        detalle_data: Show emítidos en Dicciembre del 2022.

    Return
        Cantidad de show de tv segmentado por género.
    """
    dominios = detalle_data.officialSite.unique().tolist()

    return dominios


def calcular_runtime_promedio(detalle_data: pd.DataFrame) -> float:
    """ Calcula el runtime promedio teniendo en cuenta todos los shows que poseen runtime del mes
    de Dicciembre del 2022

    Args:
        detalle_data: Show emítidos en Dicciembre del 2022.

    Return:
        runtime promedio.

    Nota esta pregunta aunque fácil, puede tener varias interpretaciones y formas
    de cálculo.
    En los datos extraidos se encuentra el feature runtime y average runtime ¿A cuál se refiere la pregunta?

    En analítica lo aconsejable es calcular la mediana como valor medio, ya que
    es una medida robusta de centralidad.
    """
    runtime_promedio = detalle_data.runtime.mean()
    return runtime_promedio.roud(2)


def execute_save(datos: pd.DataFrame, name: str):
    """ Ejecuta las tareas de almacenado de información

    Args:
        datos: Datos a almacenar.
        name: Nombre con el cual se almacenaran los datos.
    """
    name_parquet_df = path.root_parquet(name)
    save_parquet(datos, name_parquet_df)

    name_profile_df = path.root_profiling(name)
    save_profile(datos, name_profile_df)

    name_profile_df = path.root_profiling(name)
    save_profile(datos, name_profile_df)


def execution_pipeline():
    start_date = datetime.date(2022, 12, 1)
    end_date = datetime.date(2022, 12, 31)
    dates = list_dates(start_date, end_date)
    lista_df_dia = []
    lista_df_det_dia = []
    for dia in dates:
        url = f"http://api.tvmaze.com/schedule/web?date={dia}"
        data = json_api(url)

        name_json = path.root_json(dia)
        save_json(data, name_json)

        df, detalle_df = transform_json_to_dataframe(data)
        lista_df_dia.append(df)
        lista_df_det_dia.append(detalle_df)

        execute_save(df, f"show_{dia}")
        execute_save(detalle_df, f"show_detalle_{dia}")

    df_consolidado = pd.concat(lista_df_dia)
    df_det_consolidado = pd.concat(lista_df_det_dia)

    execute_save(df_consolidado, f"show_consolidado")
    execute_save(df_det_consolidado, f"show_detalle_consolidado")

    show_genero = conteo_show_tv_por_genero(df_det_consolidado)
    logger.info(f"show_genero: {show_genero}")

    run_mean = calcular_runtime_promedio(df_det_consolidado)
    logger.info(f"run_mean: {run_mean}")

    dominios = lista_dominios_oficiales_show_tv(df_det_consolidado)
    logger.info(f"dominios: {dominios}")


if __name__ == '__main__':
    execution_pipeline()


