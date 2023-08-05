

class CopyTable:
    """ Copia de datos desde el bucket del S3 a tabla en Redshift."""

    consolidado_shows = ("""COPY public.consolidado_shows 
    FROM 'C:\lulobank\show_consolidado.csv' DELIMITER ';' CSV HEADER;""")

    consolidado_detalle_shows = (""" COPY public.consolidado_detalle_shows 
    FROM 'C:\lulobank\show_detalle_consolidado.csv' DELIMITER ';' CSV HEADER;""")
