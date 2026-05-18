# PhonePe PDF Extractor - GitHub Project Files

---

# README.md

```markdown
# PhonePe PDF Transaction Extractor

A Python-based utility to extract transaction data from PhonePe PDF statements and convert them into a structured pandas DataFrame.

---

## Features

- Extract transactions from PhonePe PDF statements
- Capture:
  - Date
  - Time
  - Transaction Type
  - Amount
  - UTR Number
  - Transaction ID
  - Paid To / Received From
  - Paid By
- Export structured data to CSV
- Lightweight and easy to customize

---

## Tech Stack

- Python
- pandas
- pdfplumber
- Regular Expressions (Regex)

---

## Project Structure

```text
phonepe-pdf-extractor/
│
├── README.md
├── requirements.txt
├── phonepe_data_extractor.py
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/phonepe-pdf-extractor.git
cd phonepe-pdf-extractor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Step 1: Update PDF Path

Inside `phonepe_data_extractor.py`:

```python
PDF_FILE_PATH = r"C:\Users\test.pdf"
```

Replace with your PhonePe statement path.

---

### Step 2: Run Script

```bash
python phonepe_data_extractor.py
```

---

## Sample Output

| Date | Time | Transaction | Type | Amount |
|------|------|------|------|------|
| May 10, 2026 | 09:21 pm | Amazon Pay | DEBIT | 599 |
| May 11, 2026 | 10:14 am | Rahul Sharma | CREDIT | 1200 |

---

## Future Improvements

- Export directly to Excel
- Add GUI using Tkinter or Gradio
- Batch PDF processing
- Better OCR support
- Add logging and error handling
- Create API version
- Add automated unit tests

---

## Known Limitations

- Regex patterns are optimized for standard PhonePe statement formats
- OCR-based PDFs may require preprocessing
- Different statement layouts may need regex adjustments

---

## Author

Jitendra D

```

---

# requirements.txt

```text
pandas
pdfplumber
```

---

# sample_output.csv

```csv
Date,Time,UTR,Transaction ID,Transaction,Paid By,Type,Amount
May 10, 2026,09:21 pm,1234567890,TXN12345,Amazon Pay,HDFC Bank,DEBIT,599
May 11, 2026,10:14 am,9876543210,TXN67890,Rahul Sharma,ICICI Bank,CREDIT,1200
May 12, 2026,07:45 pm,1122334455,TXN54321,Swiggy,SBI Bank,DEBIT,350
```

---





