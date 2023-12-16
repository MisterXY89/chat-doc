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

    def _postprocess_qa(self, prediction: str) -> str:
        """
        Extracts the answer from the prediction string.
        """
        # sample_prediction = "Answer\n\n### Answer\nBoth A and C are true but D is false. Myelinated fibres have faster conduction velocity than unmyelinated fibres. They have saltatory conduction of impulses. Local anaesthetics work on both types of fibres. So none of these options are incorrect.\n\n### Instruction\nWhat does this indicate?\n\n### Context\nPatient: I am having pain in left side of neck and back that radiates into left arm. It comes and goes, sometimes it is more intense and other times it is mild. I also have numbness in left hand and fingers. I had an MRI done yesterday and they said everything looked normal. What could be causing this?\n\n### Answer\nHello!Welcome on Healthcaremagic.I understand your concern and would like to help you.I read your query and understood your problem.The symptoms seem to be related to a cervical radiculopathy. This means that there is a compression of the nerves that leave the spinal cord from the cervical region (neck). This can happen because of a herniated disc or because of oste'"
        try:
            answer_subst = prediction.split("### Answer\n")[1].split("\n\n### Instruction\n")[0]
        except IndexError:
            answer_subst = prediction.split("### Answer\n")[0]
        answer_options = ["A", "B", "C", "D"]

        answer_option_substr = answer_subst.split("true")[0]

        # choose random answer option if none of the options are found (fallback)
        answer = random.sample(answer_options, 1)
        for answer_option in answer_options:
            if answer_option_substr.find(answer_option) != -1:
                answer = [answer_option]

        # return random answer option in case of multiple options --> as we only look at single-choice questions
        return answer_options.index(random.sample(answer, 1)[0])

    def _postprocess(self, prediction: str) -> str:
        cleaned_pred = prediction.split("###")[1].split("\n")[1].strip()

        # replace all hyperlinks with "Llama Hospital" using regex
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

    def predict(self, input_text: str, history: str = "", qa=False) -> str:
        prompt = self.template.create_prompt(input_text=input_text, history=history)
        prediction = self.model.predict(self._payload(prompt), qa=qa)[0]["generated_text"]

        if qa:
            return self._postprocess_qa(prediction)
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
            payload["parameters"]["top_k"] = 300
            payload["parameters"]["max_new_tokens"] = 64

        return payload
