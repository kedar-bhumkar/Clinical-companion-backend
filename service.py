from constants import *
from pydantic_models import *
from util import *
from dto import *
import json
from openai import  OpenAI
import re
import yaml
from mock_data import *
from dto import *
from typing import Dict, Any
from bot_agent_with_memory_api_ready import chat
from shared import shared_data_instance

prompt_config = any
action_config = any
def handle_message(message:Message):    
    
    return  {"response": {"html": summary}}


def handle_config(message: Message) -> Dict[str, Any]:
    print("Inside handle_config")
    print('message', message)

    # Read the action.yaml file
    with open('config/action.yaml', 'r') as file:
        prompt_config = yaml.safe_load(file)

    # Get the options for the specific entity
    entity_options = prompt_config.get(message.entity, {}).get('system-intent', {}).get('options', {})
    print("entity_options", entity_options)

    # Check if entity options are empty or not found
    if not entity_options:        
        response = {"options": {"error": "No Action has been configured"}} 
    else:
        # Prepare the response as a key-value pair
        response = {
            "options": {key: value for key, value in entity_options.items()}
        } 

    return {"response": response}

def handlemessage(message:Message):
    print("Inside handlemessage")
    print('message',message)
    global prompt_config
    global action_config
    patient_data = []

    shared_data_instance.clear()

    prompt_config = getConfig(prompts_file)
    action_config = getConfig(action_file)
    if(message.intent == "system-intent" and message.message == "auto_populate"):
        patient_data = get_patient_data(message)
    elif(message.intent == "system-intent" and message.entity == "memberlist_page"):
        patient_data = get_All_patient_summary(message.patient_ids)
    else:
        patient_data = get_Patient_Summary('1')

    response = runner(message, patient_data)
    print("response", response)

    #print("\n shared_data_instance", shared_data_instance.get_data('auto_populate'))

    # Check if the response contains HTML
    if re.search(r'<[^>]+>', response):
        return {"response": {"html": response}}
    elif message.message == "auto_populate" or shared_data_instance.get_data('auto_populate') == 'auto_populate':
        return {"response": {"auto_populate": response}}
    else:
        #return {"response": {"html": response}}
        return {"response": response}

def get_patient_data(message):
    value = []  # Changed to a list to store multiple function results
    functions = action_config[message.entity][message.intent]["functions"]
    #print("functions", functions)
    for function in functions:
        result = globals()[function]("1")
        #print("result", result)
        value.append(result)  # Append each function result to the value list
    return value


def runner(message, patient_data):
    print("Inside runner")
    user_prompt, system_prompt = create_prompt(message,patient_data)
    client = init_AI_client(message.family)

    if(message.intent == "user-intent"):
        functions = action_config[message.entity]['user-intent']["functions"]
        print("functions", functions)
        return chat(system_prompt, user_prompt, functions, message.model)
    else:
        return  generate(client,message.model, user_prompt, system_prompt)
    

def create_prompt(message,patient_data):
    print("Inside create_prompt")
    #print("2. prompt_config", prompt_config)
    system_prompt = prompt_config["system_prompt"]

    if(message.intent == "system-intent"):
        user_prompt = prompt_config["user_prompt"][message.entity][message.intent][message.message]['input']
    else:
        user_prompt = prompt_config["user_prompt"][message.entity][message.intent]['general']['input']
        #user_prompt = message.message


    print(f"user_prompt - {user_prompt}")
    if(message.intent == "system-intent"):
        if(message.message == "auto_populate"):
            print(f"message.form_data - {message.form_data}")
            user_prompt = user_prompt.format(patient_data=patient_data, format= prompt_config["user_prompt"][message.entity][message.intent][message.message]["output"], rules=prompt_config["user_prompt"][message.entity][message.intent][message.message]["rules"], form_data=message.form_data)
        else:
            user_prompt = user_prompt.format(patient_data=patient_data, format= prompt_config["user_prompt"][message.entity][message.intent][message.message]["output"], rules=prompt_config["user_prompt"][message.entity][message.intent][message.message]["rules"])
    else:
        print(f"message.form_data - {message.form_data}")
        output = prompt_config["user_prompt"][message.entity][message.intent]['general']["output"]
        print(f"output - {output}")      
        user_prompt = user_prompt.format(patient_data=patient_data, format=output, rules=prompt_config["user_prompt"][message.entity][message.intent]['general']["rules"], question=message.message, form_data=message.form_data)
        user_prompt = user_prompt.replace("{format}", output)
    
    print("\n user_prompt", user_prompt)
    print("\n system_prompt", system_prompt)
    return user_prompt, system_prompt


def init_AI_client(model_family):    
    
    config = getConfig(config_file)   
    key = config[model_family]["key"]
    base_url = config[model_family]["url"]
    
    shared_data_instance.set_data('key', key)
    shared_data_instance.set_data('base_url', base_url)

    return OpenAI(
        api_key  = key,
        base_url = base_url
    )    


def generate(client,model,user_prompt, system_prompt):        
    num_tokens_from_string(''.join([system_prompt, user_prompt]), default_encoding, "input")
    
    chat_completion = client.chat.completions.create(
      messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        model=model,
        temperature = default_temperature
        
    )
    response = chat_completion.choices[0].message.content
    #print("response",response)
    num_tokens_from_string(response, default_encoding, "output")
    return response



