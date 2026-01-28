![Python](https://img.shields.io/badge/Python-3.x-blue)
![Parserdata API](https://img.shields.io/badge/Parserdata-API-green)

# Parserdata: Batch Invoice Extraction with Python

This example shows how to extract **structured invoice data** from a **folder of PDF / image invoices** using the [Parserdata](https://parserdata.com/parserdata-api) API.

You point the script at a folder, it uploads each invoice to the `/v1/extract` endpoint, and prints back clean JSON with the extracted fields.

---

## What this example does

- Reads all files from a folder that match a pattern (e.g. `~/Downloads/invoices/*`)
- Filters to supported file types: **PDF, PNG, JPG, JPEG**
- Sends each file to the Parserdata API with a natural language **prompt**
- Prints a structured JSON result for each invoice (invoice number, date, supplier, total, line items, etc.)
- Shows basic error handling and debugging output

---

## Requirements

- Python **3.8+**
- A Parserdata API key (starts with `pd_live_...`)

---

### 1. Clone this repository

```bash
git clone https://github.com/parserdata/parserdata-python-invoice-batch.git
cd parserdata-python-invoice-batch
```

### 2. Install dependencies
We recommend using a virtual environment, but it's optional.

```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set your API key
You can set your API key as an environment variable:

macOS / Linux:
```
export PARSERDATA_API_KEY="pd_live_..."
```

Windows (PowerShell):

```
$env:PARSERDATA_API_KEY="pd_live_..."
```

Or you can hard-code it in the script (for quick tests only), but avoid committing your key to GitHub.

### 4. Put some invoices in a folder

Create a folder with your test invoices, for example:

- C:\Users\YourName\Downloads\invoices\ (Windows)

- /Users/yourname/Downloads/invoices/ (macOS)

The script will pick up files with these extensions: .pdf, .png, .jpg, .jpeg

### 5. Configure the input folder in the script

Open invoice_folder_extractor.py and adjust this line:

```
INPUT_GLOB = r"C:\Users\Admin\Downloads\invoices\*"
```

#### Examples:

- Windows: INPUT_GLOB = r"C:\Users\YourName\Downloads\invoices\*"

- macOS / Linux: INPUT_GLOB = "/Users/yourname/Downloads/invoices/*"

### 6. Run the script

From the project root:

```
python invoice_folder_extractor.py
```

You should see output like:

```
=== invoice-001.pdf ===
Status: 200
{
  "invoice_number": "INV-001",
  "invoice_date": "2024-01-10",
  "supplier_name": "ACME Supplies",
  "total_amount": 1234.56,
  "line_items": [
    {
      "description": "Widget A",
      "quantity": 10,
      "unit_price": 12.34,
      "net_amount": 123.4
    }
  ]
}
```

If there's an error, you'll see:

```
=== invoice-001.pdf ===
Status: 400
Error body: { ... }
```

### 7. How the prompt works

In this example, we use a natural language prompt:

```
PROMPT = (
    "Extract invoice number, invoice date, supplier name, total amount, and line items "
    "(description, quantity, unit price, net amount)."
)
```

You can change this to match your use case:

- Add/remove fields

- Request alternative names

- Ask for currency codes, tax amounts, etc.

For stricter outputs, you can switch to schema mode in the API. This example keeps it simple and just uses a prompt.

### 8. Common issues

- 401 / 403 errors
  
Double-check your API key and that it's set in PARSERDATA_API_KEY.

- Timeouts
  
Default timeout is 300 seconds per request in this script. You can reduce it if needed:
```
r = requests.post(..., timeout=60)
```

- No files found
  
Check INPUT_GLOB and make sure the path and pattern match where your invoices actually are.

### 9. Next steps

- Pipe results into a database or a CSV instead of printing

- Wrap the logic into a function and reuse it from another app

- Combine with automation tools (Zapier, Make, n8n, etc.) for fully automated flows

## License

MIT – feel free to copy and adapt this example.
