# Chat-Doc App

<!-- ADD SCREENSHOT -->

## Run it yourself
To run the app locally, you can use the following command in your terminal:
```bash
python cli.py run-app port=5000 debug=True
```

Alternatively, you can run the app using Python directly:

```python
from chat_doc.app.app import App

app = App()
app.run(port = args.port, debug = args.debug)
```
## Tech-Stack

## Libraries Used

<table>
  <tr>
    <!-- Flask -->
    <td align="center" valign="middle">
      <img src="https://flask.palletsprojects.com/en/3.0.x/_images/flask-horizontal.png" alt="Flask" height="50"/>
      <br>Flask
    </td>
    <!-- Tailwind CSS -->
    <td align="center" valign="middle">
      <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Tailwind_CSS_logo.svg/1024px-Tailwind_CSS_logo.svg.png" alt="Tailwind CSS" height="50"/>
      <br>Tailwind CSS
    </td>
    <!-- daisyUI -->
    <td align="center" valign="middle">
      <img src="https://daisyui.com/images/daisyui-logo/daisyui-logomark-1024-1024.png" alt="daisyUI" height="50"/>
      <br>daisyUI
    </td>
  </tr>
</table>



The app uses Flask, Tailwind CSS, and daisyUI.
This combination is selected for its efficiency and compatibility with our existing Python codebase.
- Flask offers a lightweight and modular framework for web development,
- Tailwind and daisyUI provide a modern, responsive UI design.

**Why not NextJS?**
We opted for Flask over NextJS to leverage the seamless integration with our all-Python codebase.
This decision allows for the interoperability and reuse of configuration classes, and the convenience of importing existing modules. Thus, our architecture supports importing and running modules from external sources (refer to the 'Get-Started' section for more details).

## Retrieval Augmented Generation
The app also incperates 'Retrieval Augmented Generation' (RAG), based on the WHO's ICD-11 framework, to enhance user query assistance.
This functionality is powered locally using a SQLite database and a version of the llama.cpp model, ensuring efficiency.

## Model Inference
For model inference, we utilize a Huggingface endpoint, as our model is already hosted on the Huggingface platform.
This setup offers several advantages:

- The model starts from a paused state and becomes active on demand, ensuring resource efficiency.
- Hosting is managed on AWS in the eu-west-1 region.
- We use GPU instances (Nvidia A10G, 1x GPU, 24 GB) for fast and reliable performance.
- Cost is avg. $1.3 per hour.


## Chat-Doctor Model
The core of the Chat-Doc app is a finely-tuned 7B-Llama-2-HF model.
This advanced language model was specifically adapted to improve its ability and knowledge in medical diagnostics and advice.
Our approach involved training the model on a varried compilation of medical datasets.
These datasets were carefully selected for their relevance and depth in medical information, ensuring that the model is well-equipped to handle a wide range of medical queries.

The training was conducted on AWS, leveraging the computational power necessary to manage the model's extensive requirements.
The choice of the 7B model was strategic, balancing the need for a sophisticated understanding of medical dialogue with computational efficiency.

The fine-tuning process was detailed in [Milestone 2](/HACKING.md), where we detailed the methodology, data handling, and outcomes of the training phase.


