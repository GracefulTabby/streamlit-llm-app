from typing import TYPE_CHECKING

from langchain_core.callbacks import BaseCallbackHandler

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: "DeltaGenerator", initial_text: str = ""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)
