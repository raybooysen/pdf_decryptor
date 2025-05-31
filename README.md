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
FILENAME_PROMPT=Given the following PDF content, generate a concise, descriptive filename for the file. Ideally, include the claimant name, date, and document type. Only return the filename, do not include any explanation.\n\nPDF Content:\n{text}
```

- `MODEL` is required and specifies which OpenAI model to use for filename generation.
- `FILENAME_PROMPT` is required and controls how filenames are generated from PDF content. `{text}` will be replaced with the PDF's extracted text.

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

## Run as an API (FastAPI)

You can also run this project as a web API using FastAPI. This allows you to upload a PDF and password and receive a decrypted PDF in response.

### 1. Build the API Docker Image

```sh
docker build -f Dockerfile-API -t pdf-decryptor-api .
```

### 2. Run the API Container

```sh
docker run --rm -p 8000:8000 --env-file .env pdf-decryptor-api
```

- The API will be available at http://localhost:8000
- The `/decrypt` endpoint accepts a PDF file and password via a POST request.

### 3. Example API Usage (with curl)

```sh
curl -X POST "http://localhost:8000/decrypt" \
  -F "file=@/path/to/your/encrypted.pdf" \
  -F "password=your_pdf_password_here" \
  --output decrypted.pdf
```

- The decrypted PDF will be saved as `decrypted.pdf`.

---

## Testing the API with the Provided Script

A helper script `test_api.sh` is included to quickly test the running API using a sample PDF.

### 1. Ensure the API is Running

Start the API container as described above:

```sh
docker run --rm -p 8000:8000 --env-file .env pdf-decryptor-api
```

### 2. Run the Test Script

Make the script executable and run it:

```sh
chmod +x test_api.sh
./test_api.sh
```

- The script will POST `sample_input/pdf-test.pdf` to the API using the password from your `PDF_PASSWORD` environment variable (or a placeholder if not set).
- The decrypted PDF will be saved as `decrypted_test_output.pdf` in the current directory.

You can change the input/output filenames by editing the script if needed.

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
