from typing import Iterable, Iterator, List, TypeAlias, Union

import streamlit as st
from langchain.schema import AIMessage, HumanMessage, SystemMessage

TypeMsg: TypeAlias = AIMessage | HumanMessage | SystemMessage


class MsgProxy:
    """
    Streamlitのsession_state内でメッセージリストを管理するプロキシクラス。

    このクラスはsession_state内のメッセージリストを透過的に操作できるようにし、
    リストインターフェースを提供します。リストのような操作（追加、更新、削除等）を
    サポートし、操作結果は自動的にsession_stateに反映されます。

    Attributes:
        _key (str): session_stateで使用するキー名
        _default (List[TypeMsg]): デフォルトのメッセージリスト
    """

    def __init__(self, key: str = "messages", default: List[TypeMsg] | None = None):
        """
        プロキシを初期化します。

        Args:
            key: session_stateで使用するキー名（デフォルト: "messages"）
            default: 初期メッセージリスト（デフォルト: 空リスト）
        """
        self._key = key
        self._default = list(default) if default is not None else []

    @property
    def messages(self) -> List[TypeMsg]:
        """
        session_stateから現在のメッセージリストを取得します。

        Returns:
            現在のメッセージリスト（存在しない場合はデフォルト値を返す）
        """
        return st.session_state.get(self._key, self._default)

    @messages.setter
    def messages(self, value: List[TypeMsg]) -> None:
        """
        session_stateにメッセージリストを設定します。

        Args:
            value: 設定するメッセージリスト
        """
        st.session_state[self._key] = value
        return

    def append(self, item: TypeMsg) -> None:
        """
        メッセージをリスト末尾に追加します。

        Args:
            item: 追加するメッセージタプル（例: ("user", "こんにちは")）
        """
        messages = self.messages
        messages.append(item)
        self.messages = messages
        return

    def add_human_message(self, content: str) -> None:
        """ユーザーのメッセージを追加します。"""
        self.append(HumanMessage(content))
        return

    def add_assistant_message(self, content: str) -> None:
        """アシスタントのメッセージを追加します。"""
        self.append(AIMessage(content))
        return

    def clear(self) -> None:
        """メッセージリストを空にします。"""
        self.messages = []

    def __len__(self) -> int:
        """現在のメッセージ数を返します。"""
        return len(self.messages)

    def __getitem__(self, index: Union[int, slice]) -> TypeMsg | List[TypeMsg]:
        """指定したインデックスのメッセージを取得します。"""
        return self.messages[index]

    def __setitem__(self, index: Union[int, slice], value: TypeMsg | Iterable[TypeMsg]) -> None:
        """指定したインデックスのメッセージを更新します。"""
        messages = self.messages
        messages[index] = value  # type: ignore
        self.messages = messages
        return

    def __delitem__(self, index: Union[int, slice]) -> None:
        """指定したインデックスのメッセージを削除します。"""
        messages = self.messages
        del messages[index]
        self.messages = messages
        return

    def __iter__(self) -> Iterator[TypeMsg]:
        """メッセージリストのイテレータを返します。"""
        return iter(self.messages)

    def __repr__(self) -> str:
        """デバッグ用の文字列表現を返します。"""
        return f"MsgProxy({self.messages})"
