import logging
import shutil
import sqlite3
from pathlib import Path

## config logging ---------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
)
log = logging.getLogger('__name__')


## constants --------------------------------------------------------
ORIGINAL_DB_PATH: str = '../DBs/amciv_thesdiss_collection.sqlite'
UPDATED_DB_PATH: str = '../DBs/amciv_thesdiss_collection_fts.sqlite'


def copy_database() -> None:
    """
    Copies the SQLite database from source to destination.
    Called by manage_fts_addition().
    """
    log.debug('starting copy_database()')
    original_path = Path(ORIGINAL_DB_PATH).resolve()
    updated_path = Path(UPDATED_DB_PATH).resolve()
    if not Path(original_path).is_file():
        raise FileNotFoundError(f'source database {original_path} does not exist.')
    shutil.copy(original_path, updated_path)
    return


def apply_sql_commands() -> None:
    """
    Applies the SQL commands to create and populate the FTS5 table.
    """
    log.debug
    db_path = Path(UPDATED_DB_PATH).resolve()
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()

        ## create virtual table -------------------------------------
        log.debug('creating virtual table')
        # cursor.execute("""
        # create virtual table fts_articles using fts5(
        #   headline,
        #   content='articles', content_rowid='id'
        # );
        # """)
        cursor.execute("""
        create virtual table fts_amciv_abstracts using fts5(
          abstract,
          content='amciv_thesdiss_collection', content_rowid='id'
        );
        """)

        ## insert data ----------------------------------------------
        log.debug('inserting data')
        # print('Inserting data into FTS5 table...')
        # cursor.execute("""
        # insert into fts_articles(rowid, headline)
        #   select rowid, headline
        #   from articles;
        # """)
        cursor.execute("""
        insert into fts_amciv_abstracts(rowid, abstract)
          select rowid, abstract
          from amciv_thesdiss_collection;
        """)

        ## optimize table -------------------------------------------
        log.debug('optimizing table')
        # print('Optimizing FTS5 table...')
        # cursor.execute("insert into fts_articles(fts_articles) values('optimize');")
        cursor.execute("insert into fts_amciv_abstracts(fts_amciv_abstracts) values('optimize');")

        ## save and close -------------------------------------------
        conn.commit()
    except sqlite3.Error:
        log.exception('problem with SQL commands')
        conn.rollback()
    finally:
        conn.close()


def manage_fts_addition() -> None:
    """
    Manages the database copy and the addition of FTS5 functionality.
    Called by dundermain.
    """
    copy_database()
    apply_sql_commands()


if __name__ == '__main__':
    manage_fts_addition()
