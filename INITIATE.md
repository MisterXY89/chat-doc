# "Chat-Doc": Fine-tuning Llama2 for a medical chat-app

> Author: `Tilman Kerl` <br>
> Project Type: `Bring your own data`


Following, we present the project proposal for the course "Applied Deep Learning" at the Technical University of Vienna.
The goal of this specific project is to fine-tune Llama2 [3] model for a medical chat-application, a "Chat-Doc".

> If you want a more dense version of this proposal, see [README.md](./README.md).

## Table of Contents
<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->
- ["Chat-Doc": Fine-tuning Llama2 for a medical chat-app](#chat-doc-fine-tuning-llama2-for-a-medical-chat-app)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Data](#data)
    - [Characteristics](#characteristics)
    - [Data Store and Collection](#data-store-and-collection)
  - [Approach](#approach)
    - [Training](#training)
    - [Deployment (Application)](#deployment-application)
  - [Time Plan](#time-plan)
  - [Future Work](#future-work)
  - [References](#references)

## Introduction
<!-- why the idea-->
Getting a doctor's appointment can be a tedious task. Especially, if you are not sure if you need to see a doctor at all.
In this case, a chatbot could be a good first point of contact. It could help to assess the situation and give a recommendation on how to proceed.
Harnissing the power of NLP, a chatbot could be trained to understand the user's symptoms and give a recommendation/classification/further information on how to proceed.
Wwe propose to fine-tune the Llama2 model on a medical dataset. Llama2 is the successor of Llama2 that was trained on 2T tokens, is open-source and exhibits state-of-the-art performance on a variety of medical NLP tasks [3].

As the medical domain, and specifically medically-related questions are quite sensitive, it is important to think about how one could guarantee, firstly, that the chatbot is not biased and, secondly, that the chatbot is not giving wrong answers (haluzinations).
To adress this issue, we have various options in mind. If there is enough time, we would like to implement on of these options.
See future work for more details.

## Data
To train and develop a medical-diagnosis/doctor chatbot, it is crucial to have access to reliable, standardized data for disease classification and diagnosis. 
This data is fundamental for providing the chatbot's capability to provide accurate and up-to-date medical information.
For this, we propose the *[International Classification of Diseases, 11th Revision (ICD-11)](https://icd.who.int/browse11/l-m/en)*, which is the latest version of the World Health Organization's (WHO) International Classification of Diseases (ICD) [1].

### Characteristics
ICD-11 [1] represents a significant advancement in disease classification, marked by its transition to a computable knowledge framework, setting it apart from earlier revisions. 
This framework facilitates interoperability in digital health information environments.

ICD-11's information framework consists of three interconnected elements: the Foundation, classifications derived from the Foundation, and a common biomedical ontology linked to the Foundation.

The Foundation, the cornerstone of ICD-11, comprises approximately 80,000 entries with 40,000 synonyms. 
It characterizes diseases, syndromes, and health-related phenomena, not only descriptively but also by specifying relationships with other entities. 
The Foundation essentially functions as a semantic network, facilitating digital systems in capturing and interpreting meaning associated with each entity.


### Data Store and Collection
For our purpose we inted to collect, parse and store the data in a database. The database will most likely be hosted on AWS or GCP.
The data will be collected either:
- from the [ICD-11 Browser](https://icd.who.int/browse11/l-m/en) and parsed using the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library
- from the [ICD-11 API](https://icd.who.int/icdapi) directly (if available and feasible)


## Approach
Following, we present the approach we intend to take, for each the training, inference and deployment phase.

### Training
For the training phase, we aim to fine-tune the Llama2 model using the QLoRA technique, known as Quantized Low-Rank Adapter adaptation for pretrained language models (QLoRA). 
This method is particularly noteworthy for its efficiency in adapting a pretrained language model to specific downstream tasks.
QLoRA quantizes the model to 4 bits and attaches small "Low-Rank Adapters" for fine-tuning. 
Despite its computational efficiency, QLoRA achieves state-of-the-art results on language tasks and enables fine-tuning of models with up to 65 billion parameters on a single GPU [2].

To facilitate this training process, we will leverage the [Hugging Face Transformers library](https://huggingface.co/docs/transformers/index) [4], [Accelerate](https://huggingface.co/docs/accelerate/index), and the recently developed [PEFT](https://github.com/huggingface/peft) (Parameter Efficient Fine-tuning) [5] library by Hugging Face. 
PEFT provides techniques such as QLoRA, Prefix Tuning, Prompt Tuning, and IA3, all of which enable efficient adaptation of pre-trained language models to various downstream applications. 
This approach will ensure that our chatbot benefits from state-of-the-art model adaptation while efficiently utilizing computational resources.

Additionally, the training data will be sourced from the ICD-11 knowledge framework, enhancing the model's medical understanding and diagnostic capabilities.

### Deployment (Application)
There are two options I have in mind to embedd the trained model into an application and deploy it for a an end-user.

1. Use the trained model as a service (hosted on AWS or GCP) and providee an API to communicate with the model.
2. Embedd the model diretly in a web-app (e.g. using Flask) and provide a web-interface to communicate with the model (like Chat-GPT).

Deployment and hosting will most likely be done on AWS or GCP, both provide a variety of services to host and deploy (ML) applications. 
Additionally, both have a free tier, which should be sufficient for our purpose.

## Time Plan
Following, we present the time plan for the project: WOY (Week of Year), Days (full work days) and respective task.

| WOY | Days | Task |
| --- | --- | --- |
| 42 - 43 | 1 | Research and setup |
| 43 - 45 | 2 | Collect and parse data from ICD-11 |
| 45 - 49 | 4 | Train Llama2 using QLoRA |
| 50 - 02 | 4 | Deploy model as a service |
| 01 - 03 | 1 | Report and Presentation |
| $\sum$ | 12 |  |

12 days $\approx$ 96 hours, additional time for future work (see below) might be included.

## Future Work
As mentioned above, we would like to adress the issue of bias and wrong answers with one or more of the following approaches.
1. A (vector) database with ground-truth data (e.g. from a medical expert) to compare the chatbot's answers to and to give a confidence score/provide a source.
2. A "black-box" approach, where the chatbot is trained to detect if it is giving a wrong answer and then to ask for a second opinion from a human expert.
3. Explainability: use e.g. the [Captum](https://captum.ai/) library to provide explainability for the chatbot's answers.
4. Bias detection: employ bias detection methods to detect bias in the chatbot's answers and flag them.

## References
See also the [references.bib](./references.bib) file.

[1] Harrison, James E et al. “ICD-11: an international classification of diseases for the twenty-first century.” BMC medical informatics and decision making vol. 21,Suppl 6 206. 9 Nov. 2021, doi:10.1186/s12911-021-01534-6

[2] Dettmers, Tim, et al. "Qlora: Efficient finetuning of quantized llms." arXiv preprint arXiv:2305.14314 (2023).

[3] Touvron, Hugo, et al. "Llama 2: Open foundation and fine-tuned chat models." arXiv preprint arXiv:2307.09288 (2023).

[4] Wolf, Thomas, et al. "Transformers: State-of-the-art natural language processing." Proceedings of the 2020 conference on empirical methods in natural language processing: system demonstrations (2020).

[5] Mangrulkar, Sourab et al. "PEFT: State-of-the-art Parameter-Efficient Fine-Tuning methods" https://github.com/huggingface/peft (2022).

[6] Gugger, Sylvain, et al. "Accelerate: Training and inference at scale made simple, efficient and adaptable" https://github.com/huggingface/accelerate (2022).