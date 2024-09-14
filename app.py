import streamlit as st
import requests
from src import utils
from PIL import Image
import openai
from src.chatbot.chains import answer_with_rag

st.set_page_config(page_title="BMW's Car Assistant",
                   page_icon=":cars:")
@st.cache_data
def load_image():
    image = Image.open('./pngwing.com.png').convert("RGBA")
    return image
def main():
    image = load_image()
    st.image(image,width=50)
    st.header("Car Assistant From BMW")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    #for message in st.session_state.messages:
    #    st.chat_message(message["role"]).write(message["content"])
    prompt = st.chat_input("What is up?")
    if prompt:
        # Add user message to chat history
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response,_ = answer_with_rag(question=st.session_state.messages[-1]["content"],chat_history=st.session_state.messages[:-1])
        response = response.replace("$","\$")
        with st.chat_message("assistant"):
            st.write(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant","content":response})
        #st.chat_message("Assistant").write(response)
if __name__=="__main__":
    main()