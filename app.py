import streamlit as st
from rag_engine import engine 

st.set_page_config(page_title="MDP Group AI", page_icon="🤖")
st.title("MDP Group Kurumsal AI Asistanı")

# Sohbet geçmişini tutan bellek
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Kullanıcıdan yeni soru al
if prompt := st.chat_input("MDP Group hakkında bir soru sorun..."):
    
    # Kullanıcının sorusunu ekrana bas
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zekaya soruyu gönder ve cevabı ekrana bas
    with st.chat_message("assistant"):
        with st.spinner("düşünüyorum ."):
            answer = engine.ask_to_bot(prompt)
            st.markdown(answer, unsafe_allow_html=True)
    
    # Asistanın cevabını hafızaya kaydet
    st.session_state.messages.append({"role": "assistant", "content": answer})

    