import json
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
OUTPUT_DATA_DIR: str = '../data/'


def get_data() -> dict:
    """
    Hit's the collection-API.
    """
    amciv_collection_api_url: str = f'{BDR_COLLECTION_API_ROOT}{AMCIV_THESDISS_COLLECTION_ID}/'
    log.debug(f'amciv_collection_api_url: {amciv_collection_api_url}')
    jdict: dict = httpx.get(amciv_collection_api_url).json()
    return jdict


def inspect_data(jdict: dict) -> None:
    """
    Inspects the data.
    """
    sorted_collection_keys = sorted(jdict.keys())
    log.debug(f'sorted_collection_keys: {sorted_collection_keys}')
    sorted_item_keys = sorted(jdict['items'].keys())
    log.debug(f'sorted_item_keys: {sorted_item_keys}')
    doc_example = jdict['items']['docs'][0]
    sorted_doc_keys = sorted(doc_example.keys())
    log.debug(f'sorted_doc_keys: {sorted_doc_keys}')
    log.debug(f'doc_example: {pprint.pformat(doc_example)}')
    return


def output_data(jdict: dict) -> None:
    """
    Outputs the data.
    """
    output_path = pathlib.Path(OUTPUT_DATA_DIR) / 'amciv_thesdiss_collection.json'
    log.debug(f'output_path: {output_path}')
    output_absolute_path = output_path.resolve()
    log.debug(f'output_absolute_path: {output_absolute_path}')
    output_absolute_path.parent.mkdir(parents=True, exist_ok=True)
    json_data: str = json.dumps(jdict, sort_keys=True, indent=2)
    with open(output_absolute_path, 'w') as f:
        f.write(json_data)
    return


def run_manager() -> None:
    """
    Grabs the collection-level AmCiv Theses and Dissertations data from the BDR API.
    For all the 94 docs, it returns: ['abstract', 'json_uri', 'keyword', 'object_type', 'pid', 'primary_title', 'uri']
    For now I can use the abstract, pid, and title.
    """
    ## grab data ----------------------------------------------------
    jdict: dict = get_data()
    ## inspect it ---------------------------------------------------
    inspect_data(jdict)
    ## write data to file -------------------------------------------
    output_data(jdict)
    return


## dundermain -------------------------------------------------------
if __name__ == '__main__':
    run_manager()
