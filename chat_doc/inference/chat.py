# see inference.ipynb for now

import random
import re

from chat_doc.inference.prompt_template import PromptTemplate


class Chat(object):
    """
    Chat class --> used for chatbot inference
    needs a deployed model
    """

    template = PromptTemplate()
    model_hospital = "Lama Hospital"

    def __init__(self, model) -> None:
        self.model = model

    def _postprocess_qa(self, prediction: str, options: list) -> str:
        """
        Extracts the answer from the prediction string.
        """
        print(prediction)
        answer_options = ["A", "B", "C", "D"]

        for opt_idx, opt in enumerate(options):
            if opt in prediction:
                return opt_idx

        for answer_idx, answer_opt in enumerate(answer_options):
            answer_opt_str_1 = f" {answer_opt} "
            answer_opt_str_2 = f"{answer_opt})"
            if answer_opt_str_1 in prediction or answer_opt_str_2 in prediction:
                return answer_idx

        return random.randint(0, 3)

    def _postprocess(self, prediction: str) -> str:
        try:
            cleaned_pred = prediction.split("###")[1].split("\n")[1].strip()
        except IndexError:
            cleaned_pred = prediction.strip()

        # replace all hyperlinks with "Llama Hospital" using regex
        # regex from https://gist.github.com/gruber/8891611
        cleaned_pred = re.sub(
            r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))',
            self.model_hospital,
            cleaned_pred,
        )

        # any personal (names) and entitiy-artifacts from training
        cleaned_pred = re.sub(r"(Regards|Thanks).*", r"\1, Dr. Chad", cleaned_pred)

        cleaned_pred = cleaned_pred.replace("HCM", self.model_hospital)
        cleaned_pred = cleaned_pred.replace("Healthcaremagic", self.model_hospital)
        cleaned_pred = cleaned_pred.replace("icliniq", self.model_hospital)

        # double spaces
        cleaned_pred = re.sub(" +", " ", cleaned_pred)

        # replace ".<ABab> with .\s ...
        # e.g. Hello!Welcome to Llama Hospital.Di...
        cleaned_pred = re.sub(r"(\b\w+[.?!])(\w)", r"\1 \2", cleaned_pred)

        return cleaned_pred

    def predict(self, input_text: str, history: str = "", qa=False, row=None) -> str:
        print(input_text)
        prompt = self.template.create_prompt(input_text=input_text, history=history)
        prediction = self.model.predict(self._payload(prompt, qa=qa))[0]["generated_text"]

        if qa:
            answer = self._postprocess_qa(
                self._postprocess(prediction), options=[row.opa, row.opb, row.opc, row.opd]
            )
            print("----")
            print(answer)
            print(row.cop)
            print("---------------")
            return answer
        return self._postprocess(prediction)

    def _payload(self, prompt: str, qa: bool) -> dict:
        """
        Create payload for inference
        """
        payload = {
            "inputs": prompt,
            "parameters": {
                "do_sample": True,
                "top_p": 0.92,
                "temperature": 0.5,
                "top_k": 500,
                "max_new_tokens": 256,
                "repetition_penalty": 1.1,
                "stop": ["<</SYS>>"],
            },
        }
        # override parameters for qa --> single-choice questions
        if qa:
            payload["parameters"]["do_sample"] = False
            payload["parameters"]["top_p"] = 0.99
            payload["parameters"]["top_k"] = 200
            payload["parameters"]["max_new_tokens"] = 64
            payload["parameters"]["temperature"] = 0.1

        return payload
