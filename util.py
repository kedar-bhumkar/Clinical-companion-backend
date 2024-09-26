
import json, yaml
import random
import re
from difflib import *
import tiktoken
from pydantic_models import *

import re
from datetime import datetime, timedelta

def transform_response(theFormatter,response):
    if(theFormatter != None):        
        formatted_json = globals()[theFormatter](response)        
    else:    
        formatted_json = response
    
    return formatted_json



def getConfig(file_path):
    # Define the path to the YAML file
    yaml_file_path = file_path

    # Read the YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def num_tokens_from_string(string: str, encoding_name: str, type: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(f'For {type} the no of tokens are {num_tokens}')
    return num_tokens