# "Chat-Doc": Fine-tuning Llama2 for a medical chat-app

> Author: `Tilman Kerl` <br>
> Project Type: `Bring your own data` <br>
> Domain `Natural Language Processing`

Following, we present the project proposal for the course "Applied Deep Learning" at the Technical University of Vienna.
The goal of this specific project is to fine-tune Llama2 model for a medical chat-application, a "Chat-Doc".

> If you want to read the proposal of this project, please see [INITIATE.md](https://github.com/MisterXY89/chat-doc/blob/main/INITIATE.md).

## Project Idea
The project aims to fine-tune the Llama2 model for a medical chat application.
This chatbot should assist users in assessing their medical symptoms and provide recommendations or help for next steps, leveraging NLP and a reliable medical dataset. 

## Approach

### Data Collection
Utilize the International Classification of Diseases, 11th Revision (ICD-11) dataset to provide accurate and up-to-date medical information. Data will be collected from the ICD-11 Browser or API.

### Training
Fine-tune the Llama2 model using the QLoRA technique, which combines quantization and Low-Rank Adapters to adapt the model efficiently for specific medical NLP tasks.

### Deployment
Host the trained model as a service (API) on AWS or GCP, or embed it in a web app (e.g., using Flask) to provide a user-friendly interface for medical inquiries.

## Dataset
We will use the ICD-11 dataset, the latest version of the World Health Organization's International Classification of Diseases. This dataset is characterized by its computable knowledge framework, comprising approximately 80,000 entries with 40,000 synonyms, making it a reliable source of medical information for the chatbot's training and inference. Data will be collected and stored in a database hosted on AWS or GCP.

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
To address bias and accuracy concerns, we could implement approaches including a ground-truth vector-database for answer validation and confidence scoring, a system for human expert verification, integrate the explainability libraries for more transparency, and employ bias detection methods to flag biased responses.

## References
See also the [references.bib](./references.bib) file.

[1] Harrison, James E et al. “ICD-11: an international classification of diseases for the twenty-first century.” BMC medical informatics and decision making vol. 21,Suppl 6 206. 9 Nov. 2021, doi:10.1186/s12911-021-01534-6

[2] Dettmers, Tim, et al. "Qlora: Efficient finetuning of quantized llms." arXiv preprint arXiv:2305.14314 (2023).

[3] Touvron, Hugo, et al. "Llama 2: Open foundation and fine-tuned chat models." arXiv preprint arXiv:2307.09288 (2023).

[4] Wolf, Thomas, et al. "Transformers: State-of-the-art natural language processing." Proceedings of the 2020 conference on empirical methods in natural language processing: system demonstrations (2020).

[5] Mangrulkar, Sourab et al. "PEFT: State-of-the-art Parameter-Efficient Fine-Tuning methods" https://github.com/huggingface/peft (2022).

[6] Gugger, Sylvain, et al. "Accelerate: Training and inference at scale made simple, efficient and adaptable" https://github.com/huggingface/accelerate (2022).