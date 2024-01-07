import hashlib
import os
import random
import time

import requests
from flask import request

from chat_doc.config import config, logger
from chat_doc.inference.chat import Chat
from chat_doc.inference.prompt_template import PromptTemplate

chat = Chat(model=False)


def generate_chat_id(req: request):
    ip_address = req.remote_addr
    timestamp = str(time.time())
    user_agent = req.headers.get("User-Agent")

    raw_id = ip_address + timestamp + user_agent
    return hashlib.sha256(raw_id.encode()).hexdigest()[:20]


def _make_hf_request(payload):
    API_URL = "https://chdgdfk63z6o9xd8.eu-west-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Authorization": f"Bearer {config['credentials']['hf_token']}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def hf_inference(question: str, history: str):
    try:
        prompt = PromptTemplate()
        final_prompt = prompt.create_prompt(input_text=question, history=history)
        print("final_prompt", final_prompt)

        payload = chat._payload(final_prompt, qa=False)
        result = _make_hf_request(payload)
        print("result", result)

        try:
            result = chat._postprocess(result[0]["generated_text"])
            return result
        except Exception as e:
            logger.error(f"An error occurred during HF postprocessing: {e}")
            return "An error occurred while trying to fetch your answer. Please try again:)"

    except Exception as e:
        logger.error(f"An error occurred during HF inference: {e}")
        return "An error occurred while trying to fetch your answer. Please try again:)"  # or an appropriate fallback response


def update_chat_history(chat_id: str, question: str, answer: str):
    logger.info(f"Updating chat history for chat_id {chat_id}")
    pass
