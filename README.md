# 🐍 Pythonzinho

Um tutor de Python com inteligência artificial que explica tudo de um jeito bem simples, com comparação do dia a dia, exemplo de código e um mini desafio.

Projeto para quem está começando do zero. O código inteiro está em um único arquivo (`tutor.py`), comentado linha a linha.

**Acesse online:** https://pythonzinho.streamlit.app

## O que você aprende lendo o código

- Variáveis e textos
- Listas e dicionários
- `if`, `for` e `try/except`
- Como importar bibliotecas
- Como conversar com uma IA usando Python
- Por que nunca colocar senha ou chave dentro do código

## Como rodar no seu computador

**1. Baixe o projeto**

```
git clone https://github.com/iasenai1111-ux/pythonzinho.git
cd pythonzinho
```

**2. Instale as bibliotecas**

```
pip install -r requirements.txt
```

**3. Crie sua chave gratuita do Gemini**

Entre em https://aistudio.google.com/apikey com sua conta Google e clique em "Criar chave de API".

**4. Guarde a chave**

Crie uma pasta chamada `.streamlit` e, dentro dela, um arquivo `secrets.toml` com esta linha:

```
GEMINI_API_KEY = "cole_sua_chave_aqui"
```

Esse arquivo já está no `.gitignore`, então ele não vai para o GitHub.

**5. Rode**

```
streamlit run tutor.py
```

## Desafios

1. Mude o texto da variável `PERSONALIDADE` para o tutor explicar usando futebol.
2. Troque o título e o emoji da página.
3. Adicione um botão "Limpar conversa".
4. Salve todas as perguntas em um arquivo `perguntas.txt`.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `tutor.py` | O aplicativo |
| `requirements.txt` | Lista de bibliotecas |
| `index.html` | Página de apresentação (GitHub Pages) |
| `.gitignore` | Impede que a chave vá para o GitHub |
