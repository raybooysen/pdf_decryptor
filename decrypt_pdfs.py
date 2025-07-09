import os
import argparse
from PyPDF2 import PdfReader, PdfWriter
from dotenv import load_dotenv
import openai

load_dotenv()

def get_env_or_default(var, default=None):
    return os.getenv(var) if os.getenv(var) is not None else default

def get_filename_from_openai(text, client, model, prompt_template):
    prompt = prompt_template.replace("{text}", text[:2000])
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=30,
            temperature=0.2,
        )
        filename = response.choices[0].message.content.strip()
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-', '.')).rstrip()
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        return filename
    except Exception as e:
        print(f"OpenAI API failed: {e}")
        return None

def get_unique_filename(directory, filename):
    """Generate a unique filename by adding a suffix if the file already exists."""
    if not os.path.exists(os.path.join(directory, filename)):
        return filename
    
    # Split filename into name and extension
    name, ext = os.path.splitext(filename)
    counter = 1
    
    while True:
        new_filename = f"{name}_{counter}{ext}"
        if not os.path.exists(os.path.join(directory, new_filename)):
            return new_filename
        counter += 1

def process_single_pdf(input_path, filename, output_dir, password, client, model, filename_prompt):
    """Process a single PDF file: decrypt, generate filename, and save to output directory."""
    try:
        with open(input_path, 'rb') as infile:
            pdf_bytes = infile.read()
            output_stream, new_filename = decrypt_and_generate_filename(pdf_bytes, password, client, model, filename_prompt)
            
            # Only create output file if we successfully got an output_stream
            if output_stream is not None:
                if not new_filename:
                    new_filename = filename
                
                # Generate unique filename to prevent overwrites
                original_filename = new_filename
                unique_filename = get_unique_filename(output_dir, new_filename)
                output_path = os.path.join(output_dir, unique_filename)
                
                with open(output_path, 'wb') as outfile:
                    outfile.write(output_stream.read())
                
                if unique_filename != original_filename:
                    print(f"Processed: {filename} -> {unique_filename} (renamed to avoid conflict)")
                else:
                    print(f"Processed: {filename} -> {unique_filename}")
            else:
                print(f"Failed to decrypt {filename}: No output stream generated")
    except Exception as e:
        print(f"Failed to process {filename}: {e}")

def decrypt_and_generate_filename(pdf_bytes, password, client, model, prompt_template):
    try:
        import io
        infile = io.BytesIO(pdf_bytes)
        reader = PdfReader(infile)
        if reader.is_encrypted:
            reader.decrypt(password)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        first_page_text = reader.pages[0].extract_text() if reader.pages else ''
        new_filename = get_filename_from_openai(first_page_text or '', client, model, prompt_template)
        if not new_filename:
            new_filename = 'decrypted.pdf'
        output_stream = io.BytesIO()
        writer.write(output_stream)
        output_stream.seek(0)
        return output_stream, new_filename
    except Exception as e:
        print(f"Failed to decrypt PDF: {e}")
        return None, None

def main():
    parser = argparse.ArgumentParser(description="Decrypt PDFs and generate descriptive filenames using OpenAI.")
    parser.add_argument('--input', type=str, default=get_env_or_default('INPUT_DIR', 'input'), help='Directory containing encrypted PDFs')
    parser.add_argument('--output', type=str, default=get_env_or_default('OUTPUT_DIR', 'output'), help='Directory to save decrypted PDFs')
    parser.add_argument('--password', type=str, default=get_env_or_default('PDF_PASSWORD'), help='Password for encrypted PDFs (default: from .env PDF_PASSWORD)')
    parser.add_argument('--model', type=str, default=get_env_or_default('MODEL'), help='OpenAI model to use (default: from .env MODEL)')
    parser.add_argument('--filename-prompt', type=str, default=get_env_or_default('FILENAME_PROMPT'), help='Prompt template for filename generation (default: from .env FILENAME_PROMPT)')
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    password = args.password
    model = args.model
    filename_prompt = args.filename_prompt
    openai_api_key = get_env_or_default('OPENAI_API_KEY')

    if not password:
        print("PDF password must be provided via --password or PDF_PASSWORD in .env")
        exit(1)
    if not openai_api_key:
        print("OpenAI API key must be provided via OPENAI_API_KEY in .env")
        exit(1)
    if not model:
        print("Model must be provided via --model or MODEL in .env")
        exit(1)
    if not filename_prompt:
        print("Filename prompt must be provided via --filename-prompt or FILENAME_PROMPT in .env")
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
            input_path = os.path.join(input_dir, filename)
            process_single_pdf(input_path, filename, output_dir, password, client, model, filename_prompt)

if __name__ == "__main__":
    main()