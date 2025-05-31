#!/bin/zsh
# test_api.sh
# Test the pdf-decryptor-api Docker container using a sample PDF

API_URL="http://localhost:8000/decrypt"
PDF_PATH="sample_input/pdf-test.pdf"
PASSWORD="${PDF_PASSWORD:-your_pdf_password_here}"
OUTPUT_FILE="decrypted_test_output.pdf"

if [ ! -f "$PDF_PATH" ]; then
  echo "Sample PDF not found at $PDF_PATH"
  exit 1
fi

echo "Testing API with $PDF_PATH..."
curl -X POST "$API_URL" \
  -F "file=@$PDF_PATH" \
  -F "password=$PASSWORD" \
  --output "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
  echo "Test complete. Output saved to $OUTPUT_FILE"
else
  echo "Test failed."
fi
