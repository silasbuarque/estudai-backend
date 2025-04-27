# Transcrição e Resumo de Áudio

Este projeto é uma API desenvolvida com FastAPI para transcrever áudios e gerar resumos e flashcards baseados no texto transcrito.

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **Whisper**: Modelo de transcrição de áudio.
- **Groq**: API para geração de resumos e flashcards.
- **Python-dotenv**: Para carregar variáveis de ambiente de um arquivo `.env`.

## Instalação

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd transcricao-audio
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências necessárias:
   ```bash
   pip install fastapi uvicorn whisper python-dotenv requests
   ```

4. Certifique-se de criar um arquivo `.env` com a seguinte variável:
   ```env
   GROQ_API_KEY=<SUA_CHAVE_DE_API>
   ```

5. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

### `/resumir` (POST)

**Descrição**: Gera um resumo e flashcards baseados no texto fornecido.

**Request**:
```json
{
  "texto": "Texto para ser resumido."
}
```

**Response** (sucesso):
```json
{
  "resumo": "Resumo gerado do texto.",
  "flashcards": [
    {
      "pergunta": "Pergunta 1",
      "resposta": "Resposta 1"
    },
    {
      "pergunta": "Pergunta 2",
      "resposta": "Resposta 2"
    }
  ]
}
```

**Response** (erro):
```json
{
  "erro": "Mensagem de erro."
}
```

### `/transcrever` (POST)

**Descrição**: Transcreve o áudio enviado.

**Request**:
- Arquivo de áudio no formato `.webm` enviado como `multipart/form-data`.

**Response** (sucesso):
```json
{
  "transcricao": "Texto transcrito do áudio."
}
```

**Response** (erro):
```json
{
  "erro": "Mensagem de erro."
}
```

## Observações

- Certifique-se de que o modelo Whisper está configurado corretamente para o dispositivo (CPU ou GPU).
- A chave de API do Groq é necessária para a funcionalidade de resumo e flashcards.