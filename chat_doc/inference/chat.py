# see inference.ipynb for now

from chat_doc.inference.prompt_template import PromptTemplate


class Chat(object):
    """
    Chat class --> used for chatbot inference
    needs a deployed model
    """

    template = PromptTemplate()

    def __init__(self, model) -> None:
        self.model = model

    def predict(self, input_text: str, history: str = "") -> str:
        prompt = self.template.create_prompt(input_text=input_text, history=history)
        return self.model.predict(self._payload(prompt))[0]["generated_text"]

    def _payload(self, prompt: str) -> dict:
        """
        Create payload for inference
        """
        return {
            "inputs": prompt,
            "parameters": {
                "do_sample": True,
                # "do_sample": False,
                "top_p": 0.92,
                "temperature": 0.5,
                "top_k": 500,
                "max_new_tokens": 256,
                # "max_new_tokens": 512,
                "repetition_penalty": 1.1,
                # "stop": ["<|end|>"]
                "stop": ["<</SYS>>"],
            },
        }
