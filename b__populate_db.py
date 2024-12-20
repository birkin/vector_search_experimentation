import json
import logging
import pathlib
import pprint
import sqlite3

## config logging ---------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
)
log = logging.getLogger('__name__')


## constants --------------------------------------------------------
DB_PATH: str = '../DBs/amciv_thesdiss_collection.sqlite'
SOURCE_DATA: str = '../data/amciv_thesdiss_collection.json'


def load_data() -> dict:
    """
    Loads json.
    Called by manage_sqlite_populate().
    """
    log.debug('loading data')
    source_path = pathlib.Path(SOURCE_DATA)
    api_data: dict = json.loads(source_path.read_text())
    return api_data


def build_records(api_data: dict) -> list:
    """
    Builds records, a list of lists, from the api_data.
    Each doc in api_data['items']['docs'] has most of the following fields: ['dateCreated', 'abstract', 'json_uri', 'keyword', 'object_type', 'pid', 'primary_title', 'uri']
        - 'dateCreated' and 'abstract' are only in some of the docs.
    All fields will be included in the record as-is, except for:
        - 'abstract', which is a single-item list and will be converted to a string.
        - 'keywords', which is a list and will be converted to a json-string.
    Called by manage_sqlite_populate().
    """
    log.debug('starting build_records()')
    # log.debug(f'sample first doc, ``{pprint.pformat(api_data["items"]["docs"][0])}``')
    records: list = []
    for doc in api_data['items']['docs']:
        doc_keys = sorted(doc.keys())
        for key in doc_keys:
            assert key in [
                'abstract',
                'dateCreated',
                'json_uri',
                'keyword',
                'object_type',
                'pid',
                'primary_title',
                'uri',
            ], f'key, ``{key}`` not recognized'  # found 'dateCreated' string-field
        if 'abstract' in doc.keys():
            updated_abstract = doc['abstract'][0]
        else:
            updated_abstract = ''
        if 'dateCreated' in doc.keys():
            updated_dateCreated = doc['dateCreated']
        else:
            updated_dateCreated = ''
        keywords_json = json.dumps(doc['keyword'])
        record = {
            'abstract': updated_abstract,
            'dateCreated': updated_dateCreated,
            'json_uri': doc['json_uri'],
            'keywords': keywords_json,
            'object_type': doc['object_type'],
            'pid': doc['pid'],
            'primary_title': doc['primary_title'],
            'uri': doc['uri'],
        }
        records.append(record)
    log.debug(f'first record, ``{pprint.pformat(records[0])}``')
    return records

    ## end def build_records()


def create_db_and_table() -> bool:
    """
    Creates db and table if it does not exist.
    Fields will be: ['abstract', 'json_uri', 'keywords', 'object_type', 'pid', 'primary_title', 'uri']
    The primary key will be 'pid', which is a string.
    All the other fields are strings.
    The field 'keywords' is a JSON list of strings, so will be stored as a JSON field.
    Returns True if the table was created, False otherwise.
    """
    log.debug('starting create_db_and_table()')
    ## setup paths --------------------------------------------------
    db_path = pathlib.Path(DB_PATH)
    log.debug(f'db_path: {db_path}')
    db_path_absolute = db_path.resolve()
    log.debug(f'db_path_absolute: {db_path_absolute}')
    db_path_absolute.parent.mkdir(parents=True, exist_ok=True)
    ## access the db ------------------------------------------------
    conn = sqlite3.connect(db_path_absolute)
    cursor = conn.cursor()
    ## check if table exists ----------------------------------------
    table_created: bool = False
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='amciv_thesdiss_collection'
    """)
    table_exists = cursor.fetchone() is not None
    if table_exists:
        log.debug('table already exists.')
        conn.close()
    else:  ## create the table --------------------------------------
        log.debug('Creating table...')
        cursor.execute("""
            CREATE TABLE amciv_thesdiss_collection (
                abstract TEXT,
                dateCreated TEXT,
                json_uri TEXT,
                keywords JSON,
                object_type TEXT,
                pid TEXT PRIMARY KEY,
                primary_title TEXT,
                uri TEXT
            )
        """)
        conn.commit()
        conn.close()
        table_created: bool = True
        log.debug('table created.')
    log.debug(f'table_created, ``{table_created}``')
    return table_created


def populate_db(records: list) -> None:
    """
    Populates the table with the records.
    Only called if the table has just been created.
    Called by manage_sqlite_populate().
    """
    log.debug('starting populate_db()')
    db_path = pathlib.Path(DB_PATH)
    db_path_absolute = db_path.resolve()
    conn = sqlite3.connect(db_path_absolute)
    cursor = conn.cursor()
    for record in records:
        cursor.execute(
            """
            INSERT INTO amciv_thesdiss_collection (
                abstract,
                dateCreated,
                json_uri,
                keywords,
                object_type,
                pid,
                primary_title,
                uri
            ) VALUES (
                :abstract,
                :dateCreated,
                :json_uri,
                :keywords,
                :object_type,
                :pid,
                :primary_title,
                :uri
            )
        """,
            record,
        )
    conn.commit()
    conn.close()
    log.debug('db populated')
    return

    ## end def populate_db()


def manage_sqlite_populate():
    api_data: dict = load_data()
    records: list = build_records(api_data)
    table_created: bool = create_db_and_table()
    if table_created:
        populate_db(records)
    pass


## dundermain -------------------------------------------------------
if __name__ == '__main__':
    manage_sqlite_populate()
