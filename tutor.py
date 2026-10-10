# ============================================================
#  PYTHONZINHO - o tutor que explica Python de um jeito simples
#  Para rodar no seu computador:  streamlit run tutor.py
# ============================================================

import streamlit as st          # cria a página do chat
from google import genai        # conversa com a IA do Google (Gemini)
from google.genai import types  # configurações da IA

# ---------- 1. CONFIGURAÇÕES ----------
# Lista de modelos de IA. O tutor tenta o primeiro;
# se ele estiver ocupado, tenta o próximo da lista.
MODELOS = ["gemini-3.5-flash", "gemini-3.1-flash-lite"]

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
# Criamos a lista de mensagens só uma vez, na primeira visita.
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []  # lista com tudo que já foi dito


def perguntar_para_ia(mensagens):
    """Envia a conversa inteira para a IA e devolve a resposta."""
    # A IA chama o aluno de "user" e a si mesma de "model"
    conversa = []
    for mensagem in mensagens:
        papel = "user" if mensagem["quem"] == "user" else "model"
        conversa.append({"role": papel, "parts": [{"text": mensagem["texto"]}]})

    ultimo_erro = None
    for modelo in MODELOS:  # tenta um modelo de cada vez
        try:
            resposta = cliente.models.generate_content(
                model=modelo,
                contents=conversa,
                config=types.GenerateContentConfig(system_instruction=PERSONALIDADE),
            )
            return resposta.text  # deu certo: devolve e para por aqui
        except Exception as erro:
            ultimo_erro = erro    # deu errado: guarda o erro e tenta o próximo

    # Se chegou aqui, nenhum modelo respondeu
    return (
        "Ops, não consegui responder agora. "
        "Espere um minutinho e tente de novo.\n\n"
        f"Detalhe técnico: `{ultimo_erro}`"
    )


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
        with st.spinner("Pensando..."):
            resposta = perguntar_para_ia(st.session_state.mensagens)
        st.markdown(resposta)

    # Guarda a resposta no histórico
    st.session_state.mensagens.append({"quem": "assistant", "texto": resposta})
