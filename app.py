import streamlit as st

from my_modules.utils import MsgProxy


def main():
    st.title("Hello Streamlit!")
    st.write("This is a simple example of Streamlit web app.")

    msg_proxy = MsgProxy()
    if st.button("Add message", key="add_message"):
        msg_proxy.append(("Hello", "World"))
    st.write(msg_proxy.messages)

    if st.button("reset"):
        msg_proxy.reset()
        st.rerun()

    return


if __name__ == "__main__":
    main()
