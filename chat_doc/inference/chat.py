# see inference.ipynb for now

import random

from chat_doc.inference.prompt_template import PromptTemplate


class Chat(object):
    """
    Chat class --> used for chatbot inference
    needs a deployed model
    """

    template = PromptTemplate()

    def __init__(self, model) -> None:
        self.model = model

    def _postprocess_qa(self, prediction: str) -> str:
        """
        Postprocess prediction
        """
        # sample_prediction = "Answer\n\n### Answer\nBoth A and C are true but D is false. Myelinated fibres have faster conduction velocity than unmyelinated fibres. They have saltatory conduction of impulses. Local anaesthetics work on both types of fibres. So none of these options are incorrect.\n\n### Instruction\nWhat does this indicate?\n\n### Context\nPatient: I am having pain in left side of neck and back that radiates into left arm. It comes and goes, sometimes it is more intense and other times it is mild. I also have numbness in left hand and fingers. I had an MRI done yesterday and they said everything looked normal. What could be causing this?\n\n### Answer\nHello!Welcome on Healthcaremagic.I understand your concern and would like to help you.I read your query and understood your problem.The symptoms seem to be related to a cervical radiculopathy. This means that there is a compression of the nerves that leave the spinal cord from the cervical region (neck). This can happen because of a herniated disc or because of oste'"
        answer_subst = prediction.split("### Answer\n")[1].split("\n\n### Instruction\n")[0]
        answer_options = ["A", "B", "C", "D"]

        answer_option_substr = answer_subst.split("true")[0]

        # choose random answer option if none of the options are found (fallback)
        answer = random.sample(answer_options, 1)
        for answer_option in answer_options:
            if answer_option_substr.find(answer_option) != -1:
                answer = [answer_option]

        # return random answer option in case of multiple options --> as we only look at single-choice questions
        return random.sample(answer, 1)[0]

    def _postprocess(self, prediction: str) -> str:
        return prediction

    def predict(self, input_text: str, history: str = "", qa=False) -> str:
        prompt = self.template.create_prompt(input_text=input_text, history=history)
        prediction = self.model.predict(self._payload(prompt))[0]["generated_text"]
        if qa:
            return self._postprocess_qa(prediction)
        return self._postprocess(prediction)

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
