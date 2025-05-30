from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Projeto(BaseModel):
    name: str
    specifications: str
    deadline: str

@app.post("/gerar-descricao")
async def gerar_descricao(projeto: Projeto):
    prompt = f"""
    Gere uma descrição clara, atrativa e finalizada corretamente, com no máximo 200 caracteres, para um projeto de marketing com base nas informações abaixo:

    Título do projeto: {projeto.name}
    Especificações desejadas: {projeto.specifications}
    Prazo de execução: {projeto.deadline}

    A descrição deve ser objetiva, envolvente e escrita como se estivesse em uma plataforma para freelancers. Não ultrapasse o limite e não deixe a frase incompleta.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    descricao = response.choices[0].message.content.strip()
    return {"descricao": descricao}
