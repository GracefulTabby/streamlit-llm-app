from typing import Iterable, Iterator, List, Optional, Tuple, Union

import streamlit as st


class MsgProxy:
    """
    Streamlitのsession_state内でメッセージリストを管理するプロキシクラス。

    このクラスはsession_state内のメッセージリストを透過的に操作できるようにし、
    リストインターフェースを提供します。リストのような操作（追加、更新、削除等）を
    サポートし、操作結果は自動的にsession_stateに反映されます。

    Attributes:
        _key (str): session_stateで使用するキー名
        _default (List[Tuple[str, str]]): デフォルトのメッセージリスト
    """

    def __init__(self, key: str = "messages", default: Optional[List[Tuple[str, str]]] = None):
        """
        プロキシを初期化します。

        Args:
            key: session_stateで使用するキー名（デフォルト: "messages"）
            default: 初期メッセージリスト（デフォルト: 空リスト）
        """
        self._key = key
        self._default = list(default) if default is not None else []

    @property
    def messages(self) -> List[Tuple[str, str]]:
        """
        session_stateから現在のメッセージリストを取得します。

        Returns:
            現在のメッセージリスト（存在しない場合はデフォルト値を返す）
        """
        return st.session_state.get(self._key, self._default)

    @messages.setter
    def messages(self, value: List[Tuple[str, str]]) -> None:
        """
        session_stateにメッセージリストを設定します。

        Args:
            value: 設定するメッセージリスト
        """
        st.session_state[self._key] = value

    def reset(self) -> None:
        """メッセージリストを空リストにリセットします。"""
        self.messages = []

    def append(self, item: Tuple[str, str]) -> None:
        """
        メッセージをリスト末尾に追加します。

        Args:
            item: 追加するメッセージタプル（例: ("user", "こんにちは")）
        """
        messages = self.messages
        messages.append(item)
        self.messages = messages

    def extend(self, items: Iterable[Tuple[str, str]]) -> None:
        """
        複数のメッセージをリスト末尾に追加します。

        Args:
            items: 追加するメッセージタプルのイテラブル
        """
        messages = self.messages
        messages.extend(items)
        self.messages = messages

    def insert(self, index: int, item: Tuple[str, str]) -> None:
        """
        指定したインデックスにメッセージを挿入します。

        Args:
            index: 挿入位置のインデックス
            item: 挿入するメッセージタプル
        """
        messages = self.messages
        messages.insert(index, item)
        self.messages = messages

    def pop(self, index: int = -1) -> Tuple[str, str]:
        """
        指定したインデックスのメッセージを削除して返します。

        Args:
            index: 削除するメッセージのインデックス（デフォルト: 最終要素）

        Returns:
            削除されたメッセージタプル
        """
        messages = self.messages
        item = messages.pop(index)
        self.messages = messages
        return item

    def clear(self) -> None:
        """メッセージリストを空にします。"""
        self.messages = []

    def __len__(self) -> int:
        """現在のメッセージ数を返します。"""
        return len(self.messages)

    def __getitem__(self, index: Union[int, slice]) -> Union[Tuple[str, str], List[Tuple[str, str]]]:
        """指定したインデックスのメッセージを取得します。"""
        return self.messages[index]

    def __setitem__(self, index: Union[int, slice], value: Union[Tuple[str, str], Iterable[Tuple[str, str]]]) -> None:
        """指定したインデックスのメッセージを更新します。"""
        messages = self.messages
        messages[index] = value  # type: ignore
        self.messages = messages

    def __delitem__(self, index: Union[int, slice]) -> None:
        """指定したインデックスのメッセージを削除します。"""
        messages = self.messages
        del messages[index]
        self.messages = messages

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        """メッセージリストのイテレータを返します。"""
        return iter(self.messages)

    def __repr__(self) -> str:
        """デバッグ用の文字列表現を返します。"""
        return f"MsgProxy({self.messages})"
