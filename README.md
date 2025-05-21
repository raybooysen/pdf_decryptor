# PDF Decryptor & Smart Renamer

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

Create a `.env` file in the project root with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
PDF_PASSWORD=your_pdf_password_here
ENCRYPTED_DIR=Encrypted
UNENCRYPTED_DIR=Unencrypted
```

- Replace `your_openai_api_key_here` with your OpenAI API key
- Replace `your_pdf_password_here` with the PDF password
- Adjust the folder names if needed

### 3. Place Your PDFs

- Put all encrypted PDFs in the folder specified by `ENCRYPTED_DIR` (default: `Encrypted`)
- Make sure the destination folder (`UNENCRYPTED_DIR`, default: `Unencrypted`) exists or will be created

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
- All decrypted and renamed PDFs will appear in the `Unencrypted` folder (or as set in `.env`).

### Optional: Override Parameters

You can override any parameter at runtime:

```sh
docker run --rm -v "$(pwd)":/app --env-file .env pdf-decryptor \
  --encrypted_dir Encrypted --unencrypted_dir Unencrypted --password G3351502
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
