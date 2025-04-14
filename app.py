
import streamlit as st
import openai
import os

# Acesso à API Key
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Painel da Lili", layout="centered")
st.title("🩺 Painel da Lili")
st.caption("Acompanhe a conversa em tempo real entre dispositivos")

# Armazenar o histórico de mensagens
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Exibir histórico
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)

# Caixa de entrada
prompt = st.chat_input("Fale com a Lili...")
if prompt:
    st.session_state.chat_history.append(("user", prompt))
    st.chat_message("user").markdown(prompt)

    with st.spinner("Lili está pensando..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": r, "content": m}
                for r, m in st.session_state.chat_history
            ],
            temperature=0.7,
        )
        reply = response.choices[0].message.content

    st.session_state.chat_history.append(("assistant", reply))
    st.chat_message("assistant").markdown(reply)
