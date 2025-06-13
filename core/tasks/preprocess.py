import re
from datetime import datetime
from transformers import pipeline
from core.models.transaction import Transaction
from core.models.statement import Statement
import logging

logger = logging.getLogger(__name__)

# 🧠 Load the BERT model for transaction categorization
try:
    bert_model = pipeline(
        "text-classification",
        model="kuro-08/bert-transaction-categorization",
        tokenizer="kuro-08/bert-transaction-categorization"
    )
except Exception as e:
    bert_model = None
    logger.warning(f"BERT model load failed: {e}")

# 🧠 Support multiple transaction formats with flexible patterns
REGEX_PATTERNS = [
    {
        "pattern": re.compile(
            r"(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<desc>.+?)\s+(?P<amount>[\d,]+\.\d{2})\s+(?P<type>CR|DR)"
        ),
        "date_format": "%d/%m/%Y",
        "has_crdr": True
    },
    {
        "pattern": re.compile(
            r"(?P<date>\d{2}-\d{2}-\d{4})\s+(?P<desc>[A-Za-z\s]+)\s+\d+\s+Rs\s(?P<amount>[\d,]+\.\d{2})"
        ),
        "date_format": "%d-%m-%Y",
        "has_crdr": False
    },
    {
        "pattern": re.compile(
            r"(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<desc>.+?)\s+(?P<amount>[\d,]+\.\d{2})"
        ),
        "date_format": "%Y-%m-%d",
        "has_crdr": False
    },
    # Add more patterns here...
]

def extract_transactions(raw_text):
    """
    Try all known patterns and extract transactions intelligently.
    """
    for parser in REGEX_PATTERNS:
        pattern = parser["pattern"]
        has_crdr = parser["has_crdr"]
        date_format = parser["date_format"]
        matches = list(pattern.finditer(raw_text))

        if not matches:
            continue  # Try next pattern

        logger.info(f"Matched {len(matches)} transactions using format: {date_format}")
        transactions = []

        for match in matches:
            try:
                date_str = match.group("date").strip()
                description = match.group("desc").strip()
                amount_str = match.group("amount").replace(",", "").strip()
                amount = float(amount_str)
                txn_date = datetime.strptime(date_str, date_format).date()

                if has_crdr:
                    txn_type = match.group("type").strip().upper()
                    is_credit = txn_type == "CR"
                else:
                    is_credit = False  # fallback for unsupported formats

                transactions.append({
                    "date": txn_date,
                    "description": description,
                    "amount": amount,
                    "is_credit": is_credit
                })
            except Exception as e:
                logger.warning(f"Transaction parse error: {e} in line: {match.group(0)}")

        if transactions:
            return transactions

    logger.warning("❌ No matching regex patterns found for transaction extraction.")
    return []


def categorize_transaction(description):
    """
    Categorize a transaction using BERT or return 'Uncategorized'.
    """
    if not bert_model:
        return "Uncategorized"

    try:
        result = bert_model(description[:256])[0]
        return result["label"]
    except Exception as e:
        logger.warning(f"Categorization failed for '{description}': {e}")
        return "Uncategorized"


def process_and_store_transactions(user, statement):
    """
    Extract, categorize, and store transactions from raw OCR text.
    """
    transactions = extract_transactions(statement.raw_text)
    logger.info(f"Processing {len(transactions)} transactions for user {user.email}")

    for txn in transactions:
        category = categorize_transaction(txn["description"])
        Transaction.objects.create(
            user=user,
            statement=statement,
            date=txn["date"],
            description=txn["description"],
            amount=txn["amount"],
            is_credit=txn["is_credit"],
            category=category
        )

    return len(transactions)
