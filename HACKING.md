# Milestone 2 - Hacking

## Table of Contents
<!-- TOC depthFrom:2 depthTo:2 withLinks:1 updateOnSave:1 orderedList:0 -->
- [Milestone 2 - Hacking](#milestone-2---hacking)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Methodology](#2-methodology)
    - [Data Collection/generation](#data-collectiongeneration)
    - [Data Preprocessing](#data-preprocessing)
    - [Model Training](#model-training)
      - [Loss-Function](#loss-function)
      - [Prompt Engineering and Tuning](#prompt-engineering-and-tuning)
    - [Inference](#inference)
  - [3. Results](#3-results)
    - [Model](#model)
    - [Qualitative Evaluation](#qualitative-evaluation)
      - [Question 1](#question-1)
        - [ChatDoc](#chatdoc)
        - [GTP-4](#gtp-4)
      - [Question 2](#question-2)
        - [ChatDoc](#chatdoc-1)
        - [GTP-4](#gtp-4-1)
      - [Conclusion](#conclusion)
    - [Quantitative Results](#quantitative-results)
      - [Methodology](#methodology)
      - [Results](#results)

## 1. Introduction
This document accompanies Milestone 2 - 'Hacking', and provides an in-depth exploration of our efforts to fine-tune llama2 for the specialized applications in medical diagnostics and advice.
We start of with a general methodology section, delineating the processes of data collection, preprocessing, and model training, before presenting the results of our efforts in the final section.

## 2. Methodology

### Data Collection/generation
As the data and its quality is quite crucial for the performance of the fine-tuned model, we put a lot of effort into the data collection and preprocessing and the setup of the data pipeline.
To guarantee maintainability and extensibility, we implemented a factory pattern, coupled with a modularized OOP approach, to ensure that the data pipeline can be easily extended and adapted to new data sources.

The data collection/generation is implemented in the [chat_doc/data_generation](chat_doc/data_generation) folder.

We prepared and implemented the following data sources:
- [ICD-11](https://icd.who.int/browse11/l-m/en) (orignially proposed, see data description in [INITIATE.md](/INITIATE.md)
<!-- - [MedMCQA](https://huggingface.co/datasets/medmcqa/viewer/default/validation)-->
- [PMC Patients](https://huggingface.co/datasets/zhengyun21/PMC-Patients)
    > PMC-Patients is a first-of-its-kind dataset consisting of 167k patient summaries extracted from case reports in PubMed Central (PMC), 3.1M patient-article relevance and 293k patient-patient similarity annotations defined by PubMed citation graph.
- [Diagnose-Me](https://www.kaggle.com/datasets/dsxavier/diagnoise-me)
    > Diagnose me is an LFQA dataset of dialogues between patients and doctors based on factual conversations from icliniq.com and healthcaremagic.com that aims to collect more than 257k of different questions and prescriptions for patients.
- [med-dialogue](https://huggingface.co/datasets/medical_dialog)
    > The MedDialog dataset (English) contains conversations (in English) between doctors and patients. It has 0.26 million dialogues. The data is continuously growing and more dialogues will be added. The raw dialogues are from healthcaremagic.com and icliniq.com. All copyrights of the data belong to healthcaremagic.com and icliniq.com.

    Tis dataset however only has 400ish english dialogues, in contrast to the 260k dialogues mentioned in the description.

### Data Preprocessing
Data Processing mostly consists of cleaning the data from e.g. links etc. and formatting it in a way that the model can understand it.
This means building prompts and adding special tokens to the data:

```python
instruction = f"### Instruction\n{instruction}"
context = f"### Context\n{context}" if len(context) > 0 else None
response = f"### Answer\n{response}"
# join all the parts together
prompt = "\n\n".join([i for i in [instruction, context, response] if i is not None])
return {
    "text": prompt,
}
```

No further preprocessing is necessary as the model is trained on the raw prompts.

See the respective dataset classes for more details.

### Model Training
As training times are quite long and the necessary GPU memory is high, we use AWS to train the model.
Because the training is quite expensive with ~ 2.5$ per hour, hyperparameter optimization is not feasible for the scope of this project.
To still provide some form of optimization, we perform prompt-engineering & -tuning to optimize the model for our specific task.
Additionally, we also provide and collect multiple data sources for future training and optimization.

<!-- two runs -->
As of now, we have trained two models, the first (13B) on the ICD-11 dataset and the other (7B) one on the "dialogue-full" dataset.

The training is implemented in the [chat_doc/training](chat_doc/training) folder.

Using the CLI, the training can be started as follows:
```bash
python cli.py train --dataset icd11 --model llama-13b --epochs 3
```

The first training run was more of a proof-of-concept and test-run to see if the 13B parameter version of llama2 is suitable for our task or if the 7B parameter version is sufficient.

Please see the table below for a comparison of the two models.

| Model | Dataset |  Epochs | Batch Size | Training Time | GPU | Training Loss |
| --- | --- | --- |  --- | --- | --- | --- | 
| llama-13b | ICD-11 |  3 | 2 | 18062 | NVIDIA A10G - 24GB | 0.0611 |
| llama-7b | dialogue-full |  2 | 3 | 18062 | NVIDIA A10G - 24GB | 1.8428 |

#### Loss-Function
The default loss function for the llama2 model is the cross-entropy loss function. We did not change it as cross-entropy is a widely-used loss function for fine-tuning language models (LLMs) because it effectively measures the difference between the predicted probability distribution and the actual distribution of the target data. This loss function is particularly advantageous for LLMs as it emphasizes learning from incorrect predictions, thereby driving the model to produce outputs that closely align with the expected human language patterns.

#### Prompt Engineering and Tuning
As hyperparameter optimization was not feasible for the scope of this project, we focused on prompt-engineering & -tuning to optimize the model for our specific task.

Every time we run inference on the model, we can pass the following parameters to the model:
```python
payload = {
    "inputs": prompt,
    "parameters": {
        # enables sampling from the model's output probability distribution,
        # rather than just taking the most likely output.
        "do_sample": True,
        # Nucleus sampling: Only considers the top 92% of the probability distribution for sampling.
        # Helps in avoiding repetition and encourages more diverse outputs.
        "top_p": 0.92,
        # Controls the randomness in the output generation.
        # A lower value (like 0.5) makes the model's outputs more deterministic.
        "temperature": 0.5,
        # Limits the sampling pool to the top 500 most likely next words.
        # Helps in focusing the generation process.
        "top_k": 500,
         # Sets the maximum length of the new tokens generated in response to the prompt.
        "max_new_tokens": 256,
        # Applies a penalty for repeating the same token, making it slightly less likely to repeat words.
        "repetition_penalty": 1.1,
        # Specifies a stop token at which the model will cease generating further tokens.^
        "stop": ["<</SYS>>"],
    },
}
```

The prompt looks like this:
```python
"<s>[INST] <<SYS>>
$system_prompt<<SYS>>
###

Previous Conversation:
'''
$history
'''

$input[/INST]

"""
```
with the system prompt being:
```python
"""As Doctor Chad, your role is to carefully assess the patient's condition based on their description.
You are an experienced physician at Lama Hospital, known for your attention to detail and thorough approach.
When responding, remember to maintain your professional demeanor as Doctor Chad. Ask clarifying questions if the patient's description is not clear or incomplete.
Your goal is to provide a thoughtful, step-by-step assessment, keeping in mind the best practices of medical consultation. Let's proceed with the patient's query:"""
```

With this structure of the prompt, with clear delineations for instructions ([INST]), system prompt, and previous conversation history, we ensure an organized and contextually aware interaction.
This format helps in maintaining continuity and relevance in the conversation, particularly important in a medical consultation scenario.

Further, the system prompt itself is written to embody the persona of "Doctor Chad," an experienced physician.
It sets a professional tone and outlines specific behavioral guidelines, like asking clarifying questions and providing a step-by-step assessment, which are crucial for realistic and responsible medical dialogue simulation.

### Inference
The inference is implemented in the [chat_doc/inference](chat_doc/inference) folder.
For our purposes, we deployed an endpoint on AWS SageMaker to serve the model an run inference on the data.

## 3. Results

The first model (13B) unfortunately overfits to the training data and is not able to generalize well, thus we decided to train a second model (7B) on a different dataset and will not be evaluating the first model further.

### Model
The final (7B) model is available on [HuggingFace](https://huggingface.co/MisterXY89/chat-doctor).
Write me a message if you want to get access to the model.

Once you are approved, you can use the huggingface library to load the model.
> **NOTE**: The model needs a GPU to run, minimum 16GB of RAM and 8GB of GPU memory.
```python
from transformers import pipeline

pipe = pipeline("text-generation", model="MisterXY89/chat-doctor")

pipe("Hi, I feel dizzy and have a headache for a few days already. Should I go the doctor?")
```



### Qualitative Evaluation

For the qualitative evaluation, we use a set of questions and compare the generated responses from the fine-tuned model with the responses from GPT-4 to get a qaualitative feeling of the quality of the fine-tuned model.
A full list of questions and responses will be found at the end of the project in the [evaluation](evaluation) folder, here are only two examples for now.

#### Question 1
"Hi, I feel dizzy and have a headache for a few days already. Should I go the doctor?"

##### ChatDoc
> 'Hello! Welcome to Lama Hospital. Dizziness can be due to many reasons like low blood pressure, anemia, electrolyte imbalance etc. If it is associated with any other symptom like nausea, vomiting, blurred vision, loss of consciousness then you should visit your doctor immediately. Otherwise you may wait for 24 hours to see if your symptoms improve. Hope this helps. Regards, Dr. Chad'
>
##### GTP-4
> I'm not a medical professional, but experiencing dizziness and a headache for several days can be concerning. It's important to consult a healthcare provider to get a proper diagnosis and treatment. These symptoms could be caused by a variety of factors, ranging from minor issues to more serious conditions. A doctor will be able to conduct the necessary examinations and provide you with the appropriate advice and care. If your symptoms are severe, worsening, or accompanied by other symptoms like vision changes, difficulty speaking, or weakness, you should seek medical attention immediately.


#### Question 2
"I have unregular pain the heart like stiches."

##### ChatDoc
> Hi, This could be related to cardiac arrhythmia (irregular heart beat) or angina pectoris (chest pain due to reduced blood supply to the heart muscles). A detailed evaluation is needed to rule out these possibilities. I would suggest you to get an ECG done first followed by a 2D echocardiography if required. Hope I have answered your query. Let me know if I can assist you further. Regards, Dr. Chad

##### GTP-4
> I'm not a doctor, but it sounds like you might be experiencing some form of chest pain. It's important to take any kind of chest pain seriously, as it can be a symptom of various health issues, some of which may be serious. Here are a few general steps you should consider:
>
> - Seek Medical Attention: If this is a new symptom, or if it's severe or accompanied by other symptoms like difficulty breathing, dizziness, or nausea, you should seek medical attention immediately. Chest pain can be a sign of conditions like heart disease, lung problems, or others that require prompt medical evaluation.
>
> -  Describe Your Symptoms Accurately: When you see a healthcare professional, describe your symptoms in detail, including how long you've been experiencing the pain, its intensity, what seems to trigger it, and if anything relieves it.
> - Lifestyle Considerations: Consider any recent lifestyle changes, stress, diet, or physical activity that might be related to your symptoms.
>
> - Follow-Up Care: Depending on the cause, your healthcare provider might recommend follow-up care, tests, or lifestyle changes to help manage or treat the underlying issue.
>
> Remember, it's always better to be safe and get any concerning symptoms checked by a healthcare professional. They can provide a proper diagnosis and treatment plan.


#### Conclusion
As we can see, the fine-tuned model is able to generate quite good responses to the questions.
For example, the response to the first question showcases that the model understands the context of the question and is able to provide a clear answer.
With these two examples it is also apparent that our fine-tuned model generates shorter responses than GTP-4, this is due to our prompt-engineering where we set the maximum length of the generated response to 256 tokens.
This is the result of our experiments with the model, where we found that the model is not able to generate good responses for longer sequences.


### Quantitative Results
In addition to the qualitative evaluation, we also want to test the knowledge of the fine-tuned model.
To do so, we use the [MedMCQA](https://huggingface.co/datasets/medmcqa/viewer/default/validation) dataset to test the model.

> "MedMCQA is a large-scale, Multiple-Choice Question Answering (MCQA) dataset designed to address real-world medical entrance exam questions."

We focus on single-choice questions and feed them to the fine-tuned model, see next on how we build the queries and evaluate the results.

#### Methodology
We use the following code to build the queries and obtain the predictions from the fine-tuned model.
```python
def build_qa_query(row):
    return f"""Please answer the {row['choice_type']}-choice question to the best of your knowledge by just returning the correct option. The subject is {row['subject_name']}.

    Question: {row['question']}
    Options:
    A) {row['opa']}
    B) {row['opb']}
    C) {row['opc']}
    D) {row['opd']}"""
```

```python
def _postprocess_qa(self, prediction: str) -> str:
        """
        Extracts the answer from the prediction string.
        """
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
```

```python
y_pred = [
    chat.predict(
        build_qa_query(row),
        qa = True
    ) for _, row in validation_samples.iterrows()

]
```

The performance can then simply be evaluated by comparing the predicted answer with the correct answer and thus treating the problem as a classification problem.

```python
from sklearn.metrics import classification_report

y_true = validation_samples.cop.tolist()
classification_report(y_true, y_pred)
```

#### Results
This is the classification report for the fine-tuned model on 100 questions from the MedMCQA dataset.

```python
              precision    recall  f1-score   support

           A       0.25      0.09      0.13        33
           B       0.47      0.28      0.35        32
           C       0.29      0.33      0.31        21
           D       0.11      0.36      0.17        14

    accuracy                           0.24       100
   macro avg       0.28      0.27      0.24       100
weighted avg       0.31      0.24      0.25       100
```

As we can see, the model performs quite poorly on the task.
This is quite counter-intuitive as the model should be able to answer the questions correctly and performs quite well on the qualitative evaluation.
A reason for this could be that the model is not able to generalize well and overfits to the training data.
Furhter investigation is needed to find the root cause of this problem.
