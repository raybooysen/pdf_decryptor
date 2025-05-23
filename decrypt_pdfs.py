import os
import argparse
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv
import openai

load_dotenv()

def get_env_or_default(var, default=None):
    return os.getenv(var) if os.getenv(var) is not None else default

def get_filename_from_openai(text, client):
    prompt_template = os.getenv("PROMPT")
    if not prompt_template:
        print("Error: PROMPT environment variable must be set in your .env file.")
        exit(1)
    model = os.getenv("MODEL")
    if not model:
        print("Error: MODEL environment variable must be set in your .env file.")
        exit(1)
    prompt = prompt_template.replace("{text}", text[:2000])
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=30,
            temperature=0.2,
        )
        print("Raw OpenAI response:", response)
        filename = response.choices[0].message.content.strip()
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-', '.')).rstrip()
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        return filename
    except Exception as e:
        print(f"OpenAI API failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Decrypt PDFs and generate descriptive filenames using OpenAI.")
    parser.add_argument('--input', type=str, default=get_env_or_default('INPUT_DIR', 'input'), help='Directory containing encrypted PDFs')
    parser.add_argument('--output', type=str, default=get_env_or_default('OUTPUT_DIR', 'output'), help='Directory to save decrypted PDFs')
    parser.add_argument('--password', type=str, default=get_env_or_default('PDF_PASSWORD'), help='Password for encrypted PDFs (default: from .env PDF_PASSWORD)')
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    password = args.password
    openai_api_key = get_env_or_default('OPENAI_API_KEY')

    if not password:
        print("PDF password must be provided via --password or PDF_PASSWORD in .env")
        exit(1)
    if not openai_api_key:
        print("OpenAI API key must be provided via OPENAI_API_KEY in .env")
        exit(1)

    client = openai.OpenAI(api_key=openai_api_key)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Delete all files in the output folder before decrypting
    for f in os.listdir(output_dir):
        file_path = os.path.join(output_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            encrypted_path = os.path.join(input_dir, filename)
            try:
                with open(encrypted_path, 'rb') as infile:
                    reader = PdfReader(infile)
                    if reader.is_encrypted:
                        reader.decrypt(password)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    # Extract text from first page for naming
                    first_page_text = reader.pages[0].extract_text() if reader.pages else ''
                    print(f"\n--- Extracted text for {filename} ---\n{first_page_text}\n--- End extracted text ---\n")
                    new_filename = get_filename_from_openai(first_page_text or '', client)
                    if not new_filename:
                        new_filename = filename
                    decrypted_path = os.path.join(output_dir, new_filename)
                    with open(decrypted_path, 'wb') as outfile:
                        writer.write(outfile)
                print(f"Decrypted: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Failed to decrypt {filename}: {e}")

if __name__ == "__main__":
    main() 