FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir PyPDF2 pycryptodome openai python-dotenv
CMD ["python", "decrypt_pdfs.py"] 