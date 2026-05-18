# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:56:31 2026

@author: 91733
"""

# -*- coding: utf-8 -*-
"""
PhonePe PDF Transaction Extractor

This script extracts transaction details from a PhonePe PDF statement
and converts them into a structured pandas DataFrame.

Author: Jitendra D
Created: May 2026
"""

# ==============================
# Import Libraries
# ==============================
import re
import pandas as pd
import pdfplumber


# ==============================
# Configuration
# ==============================
PDF_FILE_PATH = r"C:\Users\test.pdf"

# Header text to remove from extracted PDF text
HEADER_TEXT = "Date Transaction Details Type Amount"


# ==============================
# PDF Text Extraction
# ==============================
def extract_text_from_pdf(file_path):
    """
    Extracts text from all pages of a PDF file.

    Parameters
    ----------
    file_path : str
        Path to the PDF file.

    Returns
    -------
    str
        Combined text from all PDF pages.
    """

    full_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                full_text += text + "\n"

    # Remove repeated table headers
    full_text = full_text.replace(HEADER_TEXT, "")

    return full_text


# ==============================
# Transaction Extraction Logic
# ==============================
def extract_transactions(text):
    """
    Extracts transaction details from raw PhonePe statement text.

    Parameters
    ----------
    text : str
        Raw extracted PDF text.

    Returns
    -------
    pandas.DataFrame
        Structured transaction data.
    """

    results = []

    # Split transactions using date pattern
    parts = re.split(r'([A-Z][a-z]{2} \d{1,2}, \d{4})', text)

    transaction_blocks = []

    # Combine date + corresponding transaction content
    for i in range(1, len(parts) - 1, 2):
        transaction_blocks.append(parts[i] + parts[i + 1])

    # Handle any trailing text block
    if len(parts) % 2 == 0:
        transaction_blocks.append(parts[-1])

    # Process each transaction block
    for block in transaction_blocks:

        block = block.strip()

        if not block:
            continue

        # ------------------------------
        # Extract Date
        # ------------------------------
        date_match = re.search(
            r'([A-Z][a-z]{2} \d{1,2}, \d{4})',
            block
        )

        # ------------------------------
        # Extract Time
        # ------------------------------
        time_match = re.search(
            r'(\d{1,2}:\d{2}\s*[ap]m)',
            block,
            re.I
        )

        # ------------------------------
        # Extract Transaction Party
        # ------------------------------
        transaction_match = re.search(
            r'Paid to (.+?)(?=\s*₹|\s*DEBIT|\s*CREDIT|UTR|Transaction|$)',
            block
        )

        # Handle "Received from"
        if transaction_match is None:
            transaction_match = re.search(
                r'Received from (.+?)(?=\s*₹|\s*DEBIT|\s*CREDIT|UTR|Transaction|$)',
                block
            )

        transaction_name = (
            transaction_match.group(1).split("Transaction")[0].strip()
            if transaction_match else ""
        )

        # Handle malformed extraction cases
        if transaction_name in ("DEBIT", "CREDIT"):

            transaction_match = re.search(
                r'(?:Paid to|Received from|Refund from)\s+'
                r'(?:DEBIT|CREDIT)?\s*₹?\s*\d+\s*'
                r'(?:\d{1,2}:\d{2}\s*[ap]m\s*)?(.+)',
                block
            )

            transaction_name = (
                transaction_match.group(1)
                .split("Transaction")[0]
                .strip()
                if transaction_match else ""
            )

        # ------------------------------
        # Extract Paid By
        # ------------------------------
        paid_by_match = re.search(
            r'Paid by\s*(.+?)(?:\n|UTR|Transaction|$)',
            block
        )

        # ------------------------------
        # Extract Transaction Type
        # ------------------------------
        type_match = re.search(
            r'\b(DEBIT|CREDIT(?!\s*card))\b',
            block,
            re.I
        )

        # ------------------------------
        # Extract Amount
        # ------------------------------
        amount_match = re.search(
            r'₹\s?(\d+(?:,\d+)*)',
            block
        )

        # ------------------------------
        # Extract UTR Number
        # ------------------------------
        utr_match = re.search(
            r'UTR\s*No\.?\s*[:\-]?\s*([A-Za-z0-9]+)',
            block,
            re.I
        )

        # ------------------------------
        # Extract Transaction ID
        # ------------------------------
        txn_id_match = re.search(
            r'Transaction\s*ID\s*[:\-]?\s*([A-Za-z0-9]+)',
            block,
            re.I
        )

        # ------------------------------
        # Append Extracted Record
        # ------------------------------
        results.append({
            "Date": date_match.group(1) if date_match else "",
            "Time": time_match.group(1) if time_match else "",
            "UTR": utr_match.group(1) if utr_match else "",
            "Transaction ID": (
                txn_id_match.group(1)
                if txn_id_match else ""
            ),
            "Transaction": transaction_name,
            "Paid By": (
                paid_by_match.group(1).strip()
                if paid_by_match else None
            ),
            "Type": (
                type_match.group(1).upper()
                if type_match else ""
            ),
            "Amount": (
                amount_match.group(1).replace(",", "")
                if amount_match else ""
            )
        })

    return pd.DataFrame(results)


# ==============================
# Main Execution
# ==============================
def main():
    """
    Main execution function.
    """

    # Extract raw text from PDF
    raw_text = extract_text_from_pdf(PDF_FILE_PATH)

    # Convert transactions into DataFrame
    transactions_df = extract_transactions(raw_text)

    # Display output
    print(transactions_df)

    # Export to CSV if needed
    # transactions_df.to_csv("transactions.csv", index=False)


# ==============================
# Script Entry Point
# ==============================
if __name__ == "__main__":
    main()