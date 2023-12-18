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
        - [llama-7b-chat](#llama-7b-chat)
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
- [ICD-11](https://icd.who.int/browse11/l-m/en) (orignially proposed)
- [MedMCQA](https://huggingface.co/datasets/medmcqa/viewer/default/validation)
- [PMC Patients](https://huggingface.co/datasets/zhengyun21/PMC-Patients)
- ... EXTEND

### Data Preprocessing

xx

### Model Training
As training times are quite long and the necessary GPU memory is high, we use AWS to train the model.
Because the training is quite expensive with ~ 2.5$ per hour, hyperparameter optimization is not feasible for the scope of this project.
To still provide some form of optimization, we perform prompt-engineering & -tuning to optimize the model for our specific task.
Additionally, we also provide and collect multiple data sources for future training and optimization.

<!-- two runs -->
As of now, we have trained two models, the first (13B) on the ICD-11 dataset and the other (7B) one on the XXX dataset.

The training is implemented in the [chat_doc/training](chat_doc/training) folder.

Using the CLI, the training can be started as follows:
```bash
python cli.py train --dataset icd11 --model llama-13b --epochs 3
```

The first training run was more of a proof-of-concept and test-run to see if the 13B parameter version of llama2 is suitable for our task or if the 7B parameter version is sufficient.

Please see the table below for a comparison of the two models.

| Model | Dataset | Dataset Size | Epochs | Batch Size | Training Time | GPU Memory | GPU | Training Loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| llama-13b | ICD-11 | XXX | 3 | 2 | XXXX | XXX | XXX | 0.0001 |
| llama-7b | XXX | XXX | 2 | 3 | XXXX | XXX | XXX | 0.0001 |

### Inference
The inference is implemented in the [chat_doc/inference](chat_doc/inference) folder.
xxx

## 3. Results

### Model
The final model is available on [HuggingFace](https://huggingface.co/MisterXY89/chat-doctor).
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
A full list of questions and responses can be found in the [evaluation](evaluation) folder, here are only two examples.

#### Question 1
"Hi, I feel dizzy and have a headache for a few days already. Should I go the doctor?"

##### ChatDoc
> 'Hello! Welcome to Lama Hospital. Dizziness can be due to many reasons like low blood pressure, anemia, electrolyte imbalance etc. If it is associated with any other symptom like nausea, vomiting, blurred vision, loss of consciousness then you should visit your doctor immediately. Otherwise you may wait for 24 hours to see if your symptoms improve. Hope this helps. Regards, Dr. Chad'
>
##### GTP-4
> I'm not a medical professional, but experiencing dizziness and a headache for several days can be concerning. It's important to consult a healthcare provider to get a proper diagnosis and treatment. These symptoms could be caused by a variety of factors, ranging from minor issues to more serious conditions. A doctor will be able to conduct the necessary examinations and provide you with the appropriate advice and care. If your symptoms are severe, worsening, or accompanied by other symptoms like vision changes, difficulty speaking, or weakness, you should seek medical attention immediately.

<!-- ##### llama-7b-chat
>  USER: Hi, I feel dizzy and have a headache for a few days already. Should I go the doctor? ASSISTANT: 如果您已經有幾天的頭痛和晃蕩感，建議您可以考慮去看醫生。這可能是由於許多因素引起的，包括睡眠不足、飲食不規律、缺氧、感染或是壓力過大等。建議您在去看醫生之前，先記錄下您的症狀和生活習慣，以便讓醫生更好地了解您的情況。-->

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


##### llama-7b-chat


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