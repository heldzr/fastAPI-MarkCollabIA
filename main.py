from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Projeto(BaseModel):
    titulo: str
    especificacoes: str
    prazo: str

@app.post("/gerar-descricao")
async def gerar_descricao(projeto: Projeto):
    prompt = f"""
    Gere uma descrição clara e atrativa para um projeto de marketing com base nas informações abaixo:

    Título do projeto: {projeto.titulo}
    Especificações desejadas: {projeto.especificacoes}
    Prazo de execução: {projeto.prazo}

    A descrição deve ser objetiva, envolvente e escrita como se estivesse em uma plataforma para freelancers.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return {"descricao": response.choices[0].message.content}
