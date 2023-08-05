
import psycopg2
import yaml

from metadata.paths import Paths
from metadata.create_tables import CreateTable
from metadata.drop_tables import DropTable
from metadata.copytable import CopyTable


def built_dwh(cur, conn, list_table):
    for query in list_table:
        cur.execute(query)
        conn.commit()


def drop_tables(cur, conn):
    """Elimina tablas preexistentes para poder crearlas desde cero."""

    drop_table_queries = [DropTable.consolidado_shows, DropTable.consolidado_detalle_shows]
    built_dwh(cur, conn, drop_table_queries)


def create_tables(cur, conn):
    """Crea tablas provisionales y dimensionales declaradas en el script sql_queries."""

    create_table_queries = [CreateTable.consolidado_shows, CreateTable.consolidado_detalle_shows]
    built_dwh(cur, conn, create_table_queries)


def load_staging_tables(cur, conn):
    """Cargue datos de archivos almacenados en S3 en las tablas provisionales mediante las consultas
    declarado en el script sql_queries."""

    copy_table_queries = [CopyTable.consolidado_shows, CopyTable.consolidado_detalle_shows]
    built_dwh(cur, conn, copy_table_queries)


def execute_bd():
    with open(Paths.cred) as file:
        cred = yaml.full_load(file)
    cred_posgrest = cred["posgrest"]

    conn = psycopg2.connect(
        host=cred_posgrest["host"],
        user=cred_posgrest["user"],
        password=cred_posgrest["password"],
        database=cred_posgrest["database"],
    )

    cursor = conn.cursor()
    drop_tables(cursor, conn)
    create_tables(cursor, conn)
    load_staging_tables(cursor, conn)


if __name__ == '__main__':
    execute_bd()
