import requests
import json
import collections
from concurrent.futures import ThreadPoolExecutor
import os

def authenticate():
    # get the OAUTH2 token

    token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
    client_id = '11754030-fc21-4204-88cd-89e8c2a48f9a_12d03ab9-9b1d-4d3b-a262-13dba7a9c3ca'
    client_secret = '3ZHiukddMxC1Cr3KvRhihQonwNYZrUg993kpNvW4aao='
    scope = 'icdapi_access'
    grant_type = 'client_credentials'

    # set data to post
    payload = {
        'client_id': client_id, 
        'client_secret': client_secret, 
        'scope': scope, 
        'grant_type': grant_type,
    }
            
    # make request
    r = requests.post(token_endpoint, data=payload, verify=False).json()
    token = r['access_token']
    return token

def fetch_node_data(uri, token):
    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Accept-Language': 'en',
        'API-Version': 'v2',
    }

    response = requests.get(uri, headers=headers, verify=True)
    return response.json()

def parse_and_store_tree(root_uri, output_file, token=authenticate(), max_workers=4, checkpoint_interval=10):
    unified_json = {}
    processed_nodes = set()

    def recursive_parse(uri):
        nonlocal unified_json

        if uri in processed_nodes:
            return

        node_data = fetch_node_data(uri, token)
        item = collections.defaultdict(lambda: 'Key Not found')

        for key, value in node_data.items():
            item[key] = value

        title = item['title']['@value']
        ID = item['@id'].split("/")[-1]

        parents = [pt.split("/")[-1] for pt in item['parent']] if item['parent'] != 'Key Not found' else []

        children = [ct.split("/")[-1] for ct in item['child']] if item['child'] != 'Key Not found' else []

        definition = item['definition']['@value'] if item['definition'] != 'Key Not found' else None

        synonyms = [syn['label']['@value'] for syn in item['synonym']] if item['synonym'] != 'Key Not found' else []

        node_data = {
            'title': title,
            'definition': definition,
            'parents': parents,
            'children': children,
            'synonyms': synonyms
        }

        if ID == 'entity':
            unified_json = node_data
        else:
            unified_json[ID] = node_data

        processed_nodes.add(uri)

        if len(processed_nodes) % checkpoint_interval == 0:
            save_checkpoint(unified_json, output_file + '.checkpoint')

        for child_uri in children:
            child_uri = f'http://id.who.int/icd/entity/{child_uri}'
            recursive_parse(child_uri)

    def process_node(uri):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(recursive_parse, uri)]
            for future in futures:
                future.result()

    def save_checkpoint(data, checkpoint_file):
        print(f'Saving checkpoint to {checkpoint_file}')

        with open(checkpoint_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def load_checkpoint(checkpoint_file):
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as json_file:
                return json.load(json_file)
        return None

    # Check for existing checkpoints and load if available
    checkpoint_data = load_checkpoint(output_file + '.checkpoint')
    if checkpoint_data:
        unified_json = checkpoint_data

    # Ensure that the first call is done before processing children
    root_node_data = fetch_node_data(root_uri, token)
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(recursive_parse, root_uri)]
        for future in futures:
            future.result()

    process_node(root_uri)
    
    # Save the final result
    with open(output_file, 'w') as json_file:
        json.dump(unified_json, json_file, indent=4)

# Example usage:
root_uri = 'http://id.who.int/icd/entity'
output_file = 'icd_tree.json'

parse_and_store_tree(root_uri, output_file, checkpoint_interval=50)