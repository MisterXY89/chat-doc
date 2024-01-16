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
    # API_URL_V1 = "https://chdgdfk63z6o9xd8.eu-west-1.aws.endpoints.huggingface.cloud"
    API_URL = "https://pxei8lam5mc67ngq.eu-west-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def hf_postprocess(prediction):
    print("prediction", prediction)
    try:
        prediction = (
            prediction.split("<</SYS>>")[1]
            .split("[/INST]")[0]
            .replace("<<SYS>>", "")
            .replace("[INST]", "")
            .strip()
        )
    except Exception as e:
        prediction = prediction.split("<interact>")[0].strip()
        logger.error(f"An error occurred during HF postprocessing: {e}")
    return prediction


def hf_inference(question: str, history: str, icd_match: str):
    try:
        question = question.strip()

        question = f"{question}\n\n Additional information: {icd_match} \n\n"
        prompt = PromptTemplate()
        final_prompt = prompt.create_prompt(input_text=question, history=history)
        print("final_prompt", final_prompt)

        payload = chat._payload(final_prompt, qa=False)
        print(payload)
        result = _make_hf_request(payload)
        # result = "test"
        print("result", result)

        try:
            result = hf_postprocess(result[0]["generated_text"])
            return result
        except Exception as e_postprocess:
            logger.error(f"An error occurred during HF postprocessing: {e_postprocess}")
            raise e_postprocess
            # return "An error occurred while trying to fetch your answer. Please try again:)"

    except Exception as e:
        raise e
        # logger.error(f"An error occurred during HF inference: {e}")
        # return "An error occurred while trying to fetch your answer. Please try again:)"  # or an appropriate fallback response


def update_chat_history(chat_id: str, question: str, answer: str):
    logger.info(f"Updating chat history for chat_id {chat_id}")
    pass
