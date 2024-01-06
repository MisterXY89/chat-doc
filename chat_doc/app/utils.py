import hashlib
import os
import random
import time

from flask import request

from chat_doc.config import logger
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
    return ""


def hf_inference(question: str, history: str):
    try:
        prompt = PromptTemplate()
        final_prompt = prompt.create_prompt(input_text=question, history=history)

        payload = chat._payload(final_prompt)
        result = _make_hf_request(payload)

        return chat._postprocess(result)

    except Exception as e:
        logger.error(f"An error occurred during HF inference: {e}")
        return "An error occurred while trying to fetch your answer. Please try again:)"  # or an appropriate fallback response


def update_chat_history(chat_id: str, question: str, answer: str):
    pass
