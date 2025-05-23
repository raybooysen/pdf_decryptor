# PDF Decryptor & Smart Renamer

I built this because my health insurer (AIA) sends encrypted PDFs with awful filenames. This app tries to give you better names as well as decrypting

This app decrypts all password-protected PDFs in a specified folder, uses OpenAI to generate a smart filename based on the PDF content, and saves the decrypted, renamed files to a destination folder.

## Features

- Decrypts all PDFs in a source directory using a single password
- Uses OpenAI to extract a meaningful filename (claimant, date, doc type, etc.) from the PDF content
- All configuration (password, directories, API key) is via `.env` or command-line arguments
- Runs easily in Docker (no Python install required)

---

## Setup

### 1. Clone or Download the Project

### 2. Prepare Your `.env` File

A sample `.env.example` file is provided. Copy it to `.env` and fill in your values:

```sh
cp .env.example .env
```

Edit `.env` to set your OpenAI API key, PDF password, input/output directories, the OpenAI model, and the prompt for filename generation.

```sh
cp .env.example .env
```

Edit `.env` to set your OpenAI API key, PDF password, input/output directories, the OpenAI model, and the prompt for filename generation.

```sh
cp .env.example .env
```

Edit `.env` to set your OpenAI API key, PDF password, input/output directories, the OpenAI model, and the prompt for filename generation.

```
OPENAI_API_KEY=sk-...your-openai-key...
PDF_PASSWORD=your_pdf_password_here
INPUT_DIR=input
OUTPUT_DIR=output
MODEL=gpt-4.1-nano-2025-04-14
PROMPT=Given the following PDF content, generate a concise, descriptive filename for the file. Ideally, include the claimant name, date, and document type. Only return the filename, do not include any explanation.\n\nPDF Content:\n{text}
```

- `MODEL` is required and specifies which OpenAI model to use for filename generation.
- `PROMPT` is required and controls how filenames are generated from PDF content. `{text}` will be replaced with the PDF's extracted text.

### 3. Place Your PDFs

- Put all encrypted PDFs in the folder specified by `INPUT_DIR` (default: `input`)
- Make sure the destination folder (`OUTPUT_DIR`, default: `output`) exists or will be created

---

## Build and Run with Docker

### Build the Docker Image

```sh
docker build -t pdf-decryptor .
```

### Run the App

```sh
docker run --rm -v "$(pwd)":/app --env-file .env pdf-decryptor
```

- This mounts your current directory into the Docker container and loads environment variables from `.env`.
- All decrypted and renamed PDFs will appear in the `output` folder (or as set in `.env`).

### Optional: Override Parameters

You can override any parameter at runtime:

```sh
docker run --rm -v "$(pwd)":/app --env-file .env pdf-decryptor \
  --input input --output output --password your_pdf_password_here
```

---

## Customization

- Change the OpenAI model or prompt in `decrypt_pdfs.py` if you want different filename logic.
- Add more environment variables or command-line arguments as needed.

---

## Troubleshooting

- If you see empty or incorrect filenames, check that your PDFs contain extractable text (not just images). For image-based PDFs, consider adding OCR support.
- Make sure your OpenAI API key and PDF password are correct in `.env`.

---

## License

MIT
