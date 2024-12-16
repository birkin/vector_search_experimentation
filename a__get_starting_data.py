import logging
import pathlib
import pprint

import httpx

## config logging ---------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
)
log = logging.getLogger('__name__')

## disable logging for httpx
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)


## constants --------------------------------------------------------
AMCIV_THESDISS_COLLECTION_ID: str = 'bdr:tkz6xrdc'
BDR_COLLECTION_API_ROOT: str = 'https://repository.library.brown.edu/api/collections/'
STARTING_DATA_DIR: str = '../data/'


def get_data() -> None:
    """
    Grabs the collection-level AmCiv Theses and Dissertations data from the BDR API.
    For all the 94 docs, it returns: ['abstract', 'json_uri', 'keyword', 'object_type', 'pid', 'primary_title', 'uri']
    For now I can use the abstract, pid, and title.
    """
    ## grab data ----------------------------------------------------
    amciv_collection_api_url: str = f'{BDR_COLLECTION_API_ROOT}{AMCIV_THESDISS_COLLECTION_ID}/'
    log.debug(f'amciv_collection_api_url: {amciv_collection_api_url}')
    output_path = pathlib.Path(STARTING_DATA_DIR) / 'amciv_thesdiss_collection.json'
    log.debug(f'output_path: {output_path}')
    jdict: dict = httpx.get(amciv_collection_api_url).json()
    ## inspect it ---------------------------------------------------
    sorted_collection_keys = sorted(jdict.keys())
    log.debug(f'sorted_collection_keys: {sorted_collection_keys}')
    sorted_item_keys = sorted(jdict['items'].keys())
    log.debug(f'sorted_item_keys: {sorted_item_keys}')
    doc_example = jdict['items']['docs'][0]
    sorted_doc_keys = sorted(doc_example.keys())
    log.debug(f'sorted_doc_keys: {sorted_doc_keys}')
    log.debug(f'doc_example: {pprint.pformat(doc_example)}')
    ## write it to file ---------------------------------------------
    # (I'll hold off on the write until I see what I actually need.)
    return


## add dundermain
if __name__ == '__main__':
    get_data()
