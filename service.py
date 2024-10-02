from constants import *
from pydantic_models import *
from util import *
from dto import *
import json
from openai import OpenAI
import re
import yaml
from mock_data import *
from typing import Dict, Any
from bot_agent_with_memory_api_ready import chat
from shared import shared_data_instance
import aiohttp

prompt_config = {}
action_config = {}

async def handlemessage(message: Message) -> Dict[str, Any]:
    print("Inside handlemessage")
    print('message', message)
    global prompt_config
    global action_config
    patient_data = []

    shared_data_instance.clear()

    prompt_config = getConfig(prompts_file)
    action_config = getConfig(action_file)

    # Check if the message contains "@Job aid"
    job_aid_match = re.search(r'@Job aid:\s*(.*)', message.message)
    web_search_match = re.search(r'@web:\s*(.*)', message.message)
    if job_aid_match:
        user_question = job_aid_match.group(1).strip()
        return await call_job_aid_api(user_question)
    elif web_search_match:
        user_question = web_search_match.group(1).strip()
        message.message = user_question
        message.intent = "user-intent"


    if message.intent == "system-intent" and message.message == "auto_populate":
        patient_data = get_patient_data(message)
    elif message.intent == "system-intent" and message.entity == "memberlist_page":
        patient_data = get_All_patient_summary(message.patient_ids)
    else:
        patient_data = get_Patient_Summary('1')

    response = runner(message, patient_data)
    print("response", response)  

    if re.search(r'<[^>]+>', response):
        return {"html": response}
    elif message.message == "auto_populate" or shared_data_instance.get_data('auto_populate') == 'auto_populate':
        return {"auto_populate": response}
    else:
        return response

async def call_job_aid_api(user_question: str) -> Dict[str, Any]:
    endpoint = "http://127.0.0.1:8001/chat"
    headers = {
        "Content-Type": "application/json",
        "userId": "mandar.bhumkar@gmail.com"
    } 
    data = {
        "msg": user_question
    }
 

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, json=data) as response:
            if response.status == 200:
                api_response = await response.json()
                return api_response
            else:
                error_message = f"Error calling Job Aid API: {response.status}"
                return  error_message

def handle_config(message: Message) -> Dict[str, Any]:
    print("Inside handle_config")
    print('message', message)

    with open('config/action.yaml', 'r') as file:
        prompt_config = yaml.safe_load(file)

    entity_options = prompt_config.get(message.entity, {}).get('system-intent', {}).get('options', {})
    print("entity_options", entity_options)

    if not entity_options:
        response = {"options": {"error": "No Action has been configured"}}
    else:
        response = {
            "options": {key: value for key, value in entity_options.items()}
        }

    return response

def get_patient_data(message):
    value = []
    functions = action_config[message.entity][message.intent]["functions"]
    for function in functions:
        result = globals()[function]("1")
        value.append(result)
    return value

def runner(message, patient_data):
    print("Inside runner")
    user_prompt, system_prompt = create_prompt(message, patient_data)
    client = init_AI_client(message.family)

    if message.intent == "user-intent":
        functions = action_config[message.entity]['user-intent']["functions"]
        print("functions", functions)
        return chat(system_prompt, user_prompt, functions, message.model)
    else:
        return generate(client, message.model, user_prompt, system_prompt)

def create_prompt(message, patient_data):
    print("Inside create_prompt")
    system_prompt = prompt_config["system_prompt"]

    if message.intent == "system-intent":
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

def generate(client, model, user_prompt, system_prompt):        
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



