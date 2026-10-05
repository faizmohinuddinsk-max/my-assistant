import os

MODEL_PATH = os.path.join("models", "arthur.gguf")
_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        from llama_cpp import Llama
        _llm = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
    return _llm


def ask(prompt):
    
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        llm = _get_llm()
        formatted = (
            f"<|start_header_id|>user<|end_header_id|>\n{prompt}"
            f"<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        )
        output = llm(formatted, max_tokens=150, stop=["<|eot_id|>"])
        return output["choices"][0]["text"].strip()
    except Exception:
        return None