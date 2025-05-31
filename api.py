from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
import io
import os
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv
import openai
from decrypt_pdfs import get_env_or_default, get_filename_from_openai, decrypt_and_generate_filename

load_dotenv()

app = FastAPI()

@app.post("/decrypt")
def decrypt_pdf(
    file: UploadFile = File(...),
    password: str = Form(...)
):
    openai_api_key = get_env_or_default('OPENAI_API_KEY')
    if not openai_api_key:
        raise HTTPException(status_code=400, detail="OpenAI API key must be provided via OPENAI_API_KEY in .env")
    client = openai.OpenAI(api_key=openai_api_key)
    pdf_bytes = file.file.read()
    output_stream, filename = decrypt_and_generate_filename(pdf_bytes, password, client)
    if output_stream is None:
        raise HTTPException(status_code=400, detail="Failed to decrypt PDF.")
    return StreamingResponse(output_stream, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=\"{filename}\""})
