import aiohttp
from typing import Dict, Any

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
