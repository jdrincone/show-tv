
class CreateTable:
    """ Creacción de tablas en un motor de Base de datos."""

    consolidado_shows = """
    create table public.consolidado_shows(
            id text,	
            id_embedded text,
            url	text,
            name	text,
            season    text,	
            number	text,
            type	text,
            airdate  text,
            airtime text,
            airstamp   text,	
            runtime	text,
            rating_average	text,
            medium	text,
            original	text,
            _links_self	text,
            _links_show	text,
            summary	text
            );"""

    consolidado_detalle_shows = """
    CREATE TABLE IF NOT EXISTS public.consolidado_detalle_shows (
            id_embedded                 text                  NOT NULL,     
            url                         text                  NOT NULL,     
            name                        text,     
            type                        text,     
            language                    text,     
            genres                      text,     
            status                      text,     
            runtime                     text,     
            averageRuntime              text,     
            premiered                   text,     
            ended                       text,     
            officialSite                text,     
            schedule                    text,     
            rating                      text,     
            weight                      text,     
            network                     text,     
            webChannel                  text,     
            dvdCountry                  text,     
            externals                   text,     
            image                       text,     
            summary                     text,     
            updated                     text,     
            _links                      text,     
            id                          text);
    """

