
class CreateTable:
    """ Creacción de tablas en un motor de Base de datos."""

    consolidado_shows = """CREATE TABLE IF NOT EXISTS consolidado_shows(
                                        id                   integer    not null,	
                                        id_embedded          integer    not null,
                                        url	                 text,
                                        name	             text,
                                        season               integer,	
                                        number            	 float,
                                        type	             text,
                                        airdate              text,
                                        airtime              text,
                                        airstamp             text,	
                                        runtime            	 float,
                                        rating_average	     text,
                                        medium	             text,
                                        original	         text,
                                        _links_self	         text,
                                        _links_show	         text,
                                        summary	             text);"""

    consolidado_detalle_shows = """CREATE TABLE IF NOT EXISTS consolidado_detalle_shows (
                                            id_embedded                 integer               not null,	 
                                            url                         text,     
                                            name                        text,     
                                            type                        text,     
                                            language                    text,
                                            officialSite                text,
                                            weight                      text,  
                                            summary                     text,     
                                            updated                     integer,    
                                            id                          integer               not null);"""

