from metadata.create_tables import CreateTable
from metadata.drop_tables import DropTable
from metadata.inserttable import InsertTable


def built_db(cur, conn, list_table):
    for query in list_table:
        cur.execute(query)
        conn.commit()


def drop_tables(cur, conn):
    """Elimina tablas preexistentes para poder crearlas desde cero."""

    drop_table_queries = [DropTable.consolidado_shows, DropTable.consolidado_detalle_shows]
    built_db(cur, conn, drop_table_queries)


def create_tables(cur, conn):
    """Crea tablas provisionales y dimensionales declaradas en el script sql_queries."""

    create_table_queries = [CreateTable.consolidado_shows, CreateTable.consolidado_detalle_shows]
    built_db(cur, conn, create_table_queries)


def load_staging_tables(cur, conn, consolidado_shows, consolidado_detalle_shows):
    """Cargue datos a la base de datos."""

    list_consolidado_shows = consolidado_shows.to_records(index=False)
    list_consolidado_detalle_shows = consolidado_detalle_shows.to_records(index=False)

    cur.executemany(InsertTable.consolidado_shows, list_consolidado_shows)
    cur.executemany(InsertTable.consolidado_detalle_shows, list_consolidado_detalle_shows)
    conn.commit()
