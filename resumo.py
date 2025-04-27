import requests
import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv() 

GROQ_API_KEY = os.getenv("GROQ_API_KEY") # Chave de API do GroqCloud

client = Groq(
 api_key=GROQ_API_KEY,
)

def gerar_resumo_e_flashcards(texto: str) -> dict:
     
    try:
        prompt_resumo = (
            "Assuma o papel de um especilista em microserviços com mais de 10 anos de experiência. "
            "O texto abaixo é a transcrição da minha aula do curso de microserviços. "
            "Resuma o conteúdo de forma clara e objetiva, mantendo os principais conceitos e ideias. \n\n"
            f"{texto}"
        )
        
        chat_completion_resumo = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_resumo,
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        resumo = chat_completion_resumo.choices[0].message.content

        resumo = resumo.replace('*', '').strip()

        print(f"Resumo gerado: {resumo}")

        prompt_flashcards = (
            "Crie tres flashcards baseados no texto abaixo. Cada flashcard deve conter uma pergunta e uma resposta. "
            "Retorne os dados apenas no formato JSON, da seguinte forma: \n"
            "{ \n"
            "    \"flashcards\": [\n"
            "        { \n"
            "            \"pergunta\": \"Pergunta 1\", \n"
            "            \"resposta\": \"Resposta 1\" \n"
            "        }, \n"
            "        { \n"
            "            \"pergunta\": \"Pergunta 2\", \n"
            "            \"resposta\": \"Resposta 2\" \n"
            "        } \n"
            "    ] \n"
            "}\n"
            f"{resumo}"
        )

        chat_completion_flashcards = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_flashcards,
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        if not chat_completion_flashcards.choices or not chat_completion_flashcards.choices[0].message.content:
            print("Erro: Resposta do modelo está vazia ou mal formatada.")
            return None

        flashcards_json = chat_completion_flashcards.choices[0].message.content

        if not flashcards_json.strip():
            print("Erro: Resposta do modelo está vazia ou contém apenas espaços em branco.")
            return None

        if flashcards_json.startswith('```') and flashcards_json.endswith('```'):
            flashcards_json = '\n'.join(flashcards_json.split('\n')[1:-1])

        try:
            print(f"Resposta do modelo para flashcards (após limpeza): {flashcards_json}")
            flashcards = json.loads(flashcards_json).get("flashcards", [])
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            print("Conteúdo retornado:", repr(flashcards_json))
            return None

        return {
            "resumo": resumo.strip(),
            "flashcards": flashcards
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Erro ao processar resposta: {e}")
        return None