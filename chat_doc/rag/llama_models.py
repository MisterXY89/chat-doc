from llama_index import ServiceContext
from llama_index.llms import LlamaCPP


class LlamaModel:
    def __init__(
        self,
        model_url,
        model_path=None,
        temperature=0.1,
        max_new_tokens=256,
        context_window=3900,
        model_kwargs={"n_gpu_layers": 1},
        verbose=True,
    ):
        self.llm = LlamaCPP(
            model_url=model_url,
            model_path=model_path,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            model_kwargs=model_kwargs,
            verbose=verbose,
        )

    def create_service_context(self, embed_model):
        return ServiceContext.from_defaults(llm=self.llm, embed_model=embed_model)
