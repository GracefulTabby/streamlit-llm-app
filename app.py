from typing import TYPE_CHECKING

import streamlit as st
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic

from my_modules.components import llm_controller
from my_modules.config import get_settings
from my_modules.streaming import StreamHandler
from my_modules.utils import MsgProxy

if TYPE_CHECKING:
    from langchain.schema import BaseMessage

    from my_modules.models import LLMConfig


def get_response(
    llm_config: "LLMConfig", msg_proxy: MsgProxy, stream_handler: StreamHandler | None = None
) -> "BaseMessage":
    # モデルを取得する
    secret = get_settings()
    chat = ChatAnthropic(
        model=llm_config.model_name,
        temperature=llm_config.temperature,
        streaming=True,
        callbacks=[stream_handler] if stream_handler else None,
        anthropic_api_key=secret.anthropic_api_key,
    )
    # 実行する
    return chat.invoke(msg_proxy.messages)


def main():
    st.title("Simple Chatbot")

    # セッション内で有効なメッセージプロキシを初期化
    msg_proxy = MsgProxy()

    with st.sidebar:
        model_params = llm_controller()

    # リセットボタン
    st.sidebar.button("会話履歴をリセットする", key="chat_reset", on_click=msg_proxy.clear)

    # ユーザー入力
    user_input = st.chat_input("質問を入力してください")
    if user_input:
        msg_proxy.add_human_message(user_input)

    # 内部でシステムプロンプトが含まれているため、2つ以上のメッセージがある場合にのみ応答を取得する
    if not msg_proxy:
        return

    # ここまでのチャットボットの応答を表示する
    for msg in msg_proxy:
        if isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message("assistant").markdown(msg.content)
        elif isinstance(msg, SystemMessage):
            pass
        else:
            raise ValueError(f"Unexpected message type: {msg}")

    # LLMの応答をstreamingで表示する
    if user_input:
        msg_container = st.chat_message("assistant").empty()
        # メッセージをストリーミングするためのハンドラを初期化
        stream_handler = StreamHandler(msg_container)
        # モデルにリクエストを送信して応答を取得
        response = get_response(model_params, msg_proxy, stream_handler)
        msg_proxy.add_assistant_message(response.content)

    return


if __name__ == "__main__":
    st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="wide")
    main()
