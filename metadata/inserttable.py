

class InsertTable:
    """ Insertar información a tablas de una base de datos."""

    consolidado_shows = ("""INSERT INTO consolidado_shows values
                                        ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")

    consolidado_detalle_shows = ("""INSERT INTO consolidado_detalle_shows values 
                                                ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")
