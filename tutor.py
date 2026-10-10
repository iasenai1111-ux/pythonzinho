# ============================================================
#  PYTHONZINHO - o tutor que explica Python de um jeito simples
#  Para rodar no seu computador:  streamlit run tutor.py
# ============================================================

import streamlit as st          # cria a página do chat
from google import genai        # conversa com a IA do Google (Gemini)
from google.genai import types  # configurações da IA

# ---------- 1. CONFIGURAÇÕES ----------
# Nome do modelo de IA. Se der erro de "modelo não encontrado",
# troque por outro modelo gratuito, por exemplo "gemini-3.1-flash-lite".
MODELO = "gemini-3.5-flash"

# Este texto é o "jeito de ser" do tutor.
# EXPERIMENTE MUDAR e veja como as respostas mudam!
PERSONALIDADE = """
Você é o Pythonzinho, um tutor de Python para quem nunca programou.
Responda sempre em português do Brasil, com palavras simples,
como se explicasse para uma criança de 8 anos.

Use sempre este formato:
1. **Em uma frase:** a explicação mais curta possível.
2. **É como...** uma comparação com algo do dia a dia.
3. **Exemplo:** um código Python bem curto, com comentário em cada linha.
4. **Sua vez:** um mini desafio fácil para o aluno tentar.

Se a pergunta não for sobre programação, diga com gentileza
que você só sabe ajudar com Python.
"""

# ---------- 2. APARÊNCIA DA PÁGINA ----------
st.set_page_config(page_title="Pythonzinho", page_icon="🐍")
st.title("🐍 Pythonzinho")
st.caption("Pergunte qualquer coisa sobre Python. Eu explico bem devagar!")

# ---------- 3. LIGANDO A IA ----------
# A chave fica guardada em "segredos", nunca dentro do código.
chave = st.secrets["GEMINI_API_KEY"]
cliente = genai.Client(api_key=chave)

# st.session_state é a "memória" da página.
# Criamos a conversa só uma vez, na primeira visita.
if "conversa" not in st.session_state:
    st.session_state.conversa = cliente.chats.create(
        model=MODELO,
        config=types.GenerateContentConfig(system_instruction=PERSONALIDADE),
    )
    st.session_state.mensagens = []  # lista com tudo que já foi dito

# ---------- 4. MOSTRANDO O HISTÓRICO ----------
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["quem"]):
        st.markdown(mensagem["texto"])

# ---------- 5. RECEBENDO A PERGUNTA ----------
pergunta = st.chat_input("Ex.: o que é uma variável?")

if pergunta:
    # Mostra e guarda a pergunta do aluno
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"quem": "user", "texto": pergunta})

    # Pede a resposta para a IA
    with st.chat_message("assistant"):
        try:
            with st.spinner("Pensando..."):
                resposta = st.session_state.conversa.send_message(pergunta).text
        except Exception as erro:
            resposta = (
                "Ops, não consegui responder agora. "
                "Espere um minutinho e tente de novo.\n\n"
                f"Detalhe técnico: `{erro}`"
            )
        st.markdown(resposta)

    # Guarda a resposta no histórico
    st.session_state.mensagens.append({"quem": "assistant", "texto": resposta})
