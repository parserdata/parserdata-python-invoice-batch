import os
import json
import glob
import mimetypes

import requests

# 1) Read API key from environment
API_KEY = os.environ.get("PARSERDATA_API_KEY") or "API_KEY"

if not API_KEY or API_KEY == "API_KEY":
    raise RuntimeError(
        "Set the PARSERDATA_API_KEY environment variable "
        "or replace 'API_KEY' in this file with your actual key."
    )

URL = "https://api.parserdata.com/v1/extract"
HEADERS = {"X-API-Key": API_KEY}

# 2) Prompt: customize this for your needs
PROMPT = (
    "Extract invoice number, invoice date, supplier name, total amount, and line items "
    "(description, quantity, unit price, net amount)."
)

# 3) Change this to your folder of invoices
INPUT_GLOB = r"C:\Users\Admin\Downloads\invoices\*"

# Supported file extensions
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

FILE_PATHS = [
    p
    for p in glob.glob(INPUT_GLOB)
    if os.path.splitext(p)[1].lower() in ALLOWED_EXTENSIONS
]

if not FILE_PATHS:
    print("No matching files found for pattern:", INPUT_GLOB)
    raise SystemExit(1)


def extract_invoice(path: str) -> None:
    """Upload a single file to Parserdata and print the result."""
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"

    with open(path, "rb") as f:
        files = {"file": (os.path.basename(path), f, mime)}
        data = {
            "prompt": PROMPT,
            "options": json.dumps(
                {
                    "return_schema": False,
                    "return_selected_fields": False,
                }
            ),
        }

        response = requests.post(
            URL,
            headers=HEADERS,
            files=files,
            data=data,
            timeout=300,
        )

    filename = os.path.basename(path)
    print("\n===", filename, "===")
    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Error body:", response.text[:2000])
        return

    try:
        result = response.json()
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response")
        print("Raw body:", response.text[:2000])
        return

    # Print only the extracted part (less noise)
    payload = result.get("result", result)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    for path in FILE_PATHS:
        extract_invoice(path)


if __name__ == "__main__":
    main()
