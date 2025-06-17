from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o cliente da OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inicializa o FastAPI
app = FastAPI()

# Configuração do CORS
origins = [
    "https://markcollab-frontend-pi.vercel.app",  # frontend Vercel
    "http://localhost:3000"                        # ambiente local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos os métodos
    allow_headers=["*"],              # Permite todos os headers
)

# Schema para entrada
class Projeto(BaseModel):
    name: str
    specifications: str
    deadline: str

# Endpoint da IA
@app.post("/api/ia/gerar-descricao")
async def gerar_descricao(projeto: Projeto):
    prompt = f"""
    Gere uma descrição clara, atrativa e finalizada corretamente, com no máximo 350 caracteres, para um projeto que o contratate está postando com base nas informações abaixo:

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
