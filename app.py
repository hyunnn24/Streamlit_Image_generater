import streamlit
import openai 
import time
from openai import OpenAI

def APIINPUT():
    st.header("API Key를 입력하세요")
    API = st.text_input("API", type="password")
    if API:
        st.session_state.API = API


    if 'API' in st.session_state:
        st.write("API상태: 입력됨")
    else:
        st.write("API상태: 입력안됨")

def run_and_wait(client, assistant, thread):
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while True:
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(run_check.status)
        if run_check.status in ['queued', 'in_progress']:
            time.sleep(2)
        else:
            break
    return run


def drawing():
    st.header("무엇이든 그려보세요.")
    pprompt = st.text_input("프롬프트?")
    
    if 'API' in st.session_state:
        if pprompt:

            client = OpenAI(api_key=st.session_state.API)
            response = client.images.generate(model="dall-e-3", prompt=pprompt)
            image_url = response.data[0].url
            st.image(image_url)
        else:
            st.write("프롬프트를 입력하세요")
    else:
        st.write("API Key를 먼저 입력하세요.")

page = st.sidebar.selectbox("페이지 선택", ["API", "그림"])

if page == "API":
    APIINPUT()

elif page == "그림":
    drawing()
