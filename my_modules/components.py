import streamlit as st

from .models import LLMConfig


def llm_controller(key="controller") -> "LLMConfig":
    """
    UIコンポーネントとパラメータ管理
    サイドバーのコントローラを前提としている

    Returns:
        Tuple[str, float, int]: (選択されたモデル名, 温度, 最大トークン数)
    """
    model_name = st.selectbox(
        "モデル",
        [
            "claude-3-5-haiku-latest",
            "claude-3-5-sonnet-latest",
        ],
        key=f"{key}_model_name",
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, key=f"{key}_temperature")
    max_tokens = st.slider("最大トークン数", 100, 2000, 1000, key=f"{key}_max_tokens")
    return LLMConfig(model_name, temperature, max_tokens)
