import streamlit as st
import openai
import os 
# --- CONFIGURAÇÃO DA API ---
openai.api_key = os.getenv("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")

# --- FUNÇÃO PARA BUSCAR NA WIKIPEDIA ---
def buscar_wikipedia(pergunta):
    try:
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{pergunta.replace(' ', '_')}"
        resposta = requests.get(url).json()
        
        if "extract" in resposta:
            return resposta["extract"]
        else:
            return None
    except:
        return None

# --- FUNÇÃO PARA GERAR RESPOSTA COM OPENAI ---
def gerar_resposta_openai(pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": pergunta}],
            temperature=0.2
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Erro com OpenAI: {e}"

# --- FUNÇÃO PRINCIPAL DE RESPOSTA ---
def responder(pergunta):
    resposta = buscar_wikipedia(pergunta)
    if resposta:
        return resposta
    else:
        return gerar_resposta_openai(pergunta)

# --- INTERFACE STREAMLIT ---
st.title("💬 Chat com IA")

if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

# 📌 Entrada do usuário (já envia com Enter)
pergunta = st.chat_input("Digite sua pergunta:")

if pergunta:
    st.session_state["mensagens"].append(("Você", pergunta))
    resposta_texto = responder(pergunta)
    st.session_state["mensagens"].append(("IA", resposta_texto))

# 📌 Exibir histórico
for autor, msg in st.session_state["mensagens"]:
    if autor == "Você":
        st.markdown(f"**🧑 {autor}:** {msg}")
    elif autor == "IA":
        st.markdown(f"**🤖 {autor}:** {msg}")
