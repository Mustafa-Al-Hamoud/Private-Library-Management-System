import pandas as pd
from connection_string import connection_str
from sqlalchemy import create_engine, text

def load_books():
    book_df = None
    select_books ="""
                    Select 
                        c.copy_id,
                        b.title,
                        b.author,
                        b.genre,
                        c.copy_status,
                        c.purchase_price,
                        c.purchase_date
                    from copies c
                    inner join books b
                    using(book_id);
                    """                     
                 

    engine =create_engine(connection_str())
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            book_df = pd.DataFrame(connection.execute(text(select_books)))
            transaction.commit()
        except:
            transaction.rollback()
            raise
    return book_df
