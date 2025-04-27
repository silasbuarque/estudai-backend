from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from resumo import gerar_resumo_e_flashcards

import whisper
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("base", device="cpu")

@app.post("/resumir")
async def resumir_texto(request: Request):
    body = await request.json()
    texto = body.get("texto")

    if not texto:
        return JSONResponse(content={"erro": "Texto ausente no corpo da requisição"}, status_code=400)
    
    try:
        resultado = gerar_resumo_e_flashcards(texto)
        return JSONResponse(content=resultado)
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)

@app.post("/transcrever")
async def transcrever_audio(file: UploadFile = File(...)):
    print(f"🟡 Arquivo recebido: {file.filename}")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        file_bytes = await file.read()
        tmp.write(file_bytes)
        tmp_path = tmp.name

    print(f"📁 Arquivo salvo temporariamente em: {tmp_path}")

    resultado = model.transcribe(tmp_path)
    texto = resultado["text"]
     
    print("✅ Transcrição gerada:")
    print(texto)

    return JSONResponse(content={"transcricao": texto})
