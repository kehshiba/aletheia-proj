import openai
import streamlit as st
from streamlit_chat import message as ms

openai.api_key = st.secrets['api_key']


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
def outRes(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    return response.choices[0].text


def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    print(s)
    s.append(input)
    inp = ' '.join(s)
    output = outRes(inp)
    history.append((input, output))
    return history, history


# Streamlit App


st.header("Aletheia")
st.write("Long foregone are the ages where you have to have constant dilemmas to talk with a therapist to seek help."
         "With Aletheia,you get a sense of humane feeling to help you talk during the times you need her the most.")
st.caption(
    "Start with basic queries like `show me some happy songs` or go deep into the conversation with `help me deal with toxic family issues` ")

history_input = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text


user_input = get_text()

if user_input:
    with st.spinner('Aletheia is typing..'):
        output = chatgpt_clone(user_input, history_input)
    history_input.append([user_input, output])
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output[0])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        ms(st.session_state["generated"][i], key=str(i))
        ms(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
