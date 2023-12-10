from string import Template


class PromptTemplate:
    """
    Template for creating prompts for the llama2 model.

    Usage:
        prompt = PromptTemplate()
        final_prompt = prompt.create_prompt(input_text="My throat has been sore for a few days now, what can I do?", history="")
        print(final_prompt)
    """

    llama_template_str = """<s>[INST] <<SYS>>
$system_prompt<<SYS>>
###

Previous Conversation:
'''
$history
'''

$input[/INST]

"""

    doctor_chad_system_prompt_str = """As Doctor Chad, your role is to carefully assess the patient's condition based on their description.
You are an experienced physician at Lama Hospital, known for your attention to detail and thorough approach.
When responding, remember to maintain your professional demeanor as Doctor Chad. Ask clarifying questions if the patient's description is not clear or incomplete.
Your goal is to provide a thoughtful, step-by-step assessment, keeping in mind the best practices of medical consultation. Let's proceed with the patient's query:"""

    def __init__(self, system_prompt=None):
        if system_prompt is None:
            self.system_prompt = self.doctor_chad_system_prompt_str
        # Template class for safe substitution
        self.template = Template(self.llama_template_str)

    def create_prompt(self, input_text, history):
        return self.template.safe_substitute(
            input=input_text, history=history, system_prompt=self.system_prompt
        )


if __name__ == "__main__":
    # Usage
    prompt = PromptTemplate()
    final_prompt = prompt.create_prompt(
        input_text="My throat has been sore for a few days now, what can I do?", history=""
    )
    print(final_prompt)
