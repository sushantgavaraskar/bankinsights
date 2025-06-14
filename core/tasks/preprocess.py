import re
from datetime import datetime
from transformers import pipeline
from core.models.transaction import Transaction
from core.models.statement import Statement
from core.tasks.ai_service import TransactionCategorizer
import logging

logger = logging.getLogger(__name__)

# Load the BERT model for transaction categorization

bert_model = TransactionCategorizer()
#  Mapping of model output labels to real categories
LABEL_MAP = {
    "Label_0": "Utilities",
    "Label_1": "Health",
    "Label_2": "Dining",
    "Label_3": "Travel",
    "Label_4": "Education",
    "Label_5": "Subscription",
    "Label_6": "Family",
    "Label_7": "Food",
    "Label_8": "Festivals",
    "Label_9": "Culture",
    "Label_10": "Apparel",
    "Label_11": "Transportation",
    "Label_12": "Investment",
    "Label_13": "Shopping",
    "Label_14": "Groceries",
    "Label_15": "Documents",
    "Label_16": "Grooming",
    "Label_17": "Entertainment",
    "Label_18": "Social Life",
    "Label_19": "Beauty",
    "Label_20": "Rent",
    "Label_21": "Money transfer",
    "Label_22": "Salary",
    "Label_23": "Tourism",
    "Label_24": "Household",
}


# Regular expressions to match various bank statement formats
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
    # Add more patterns as needed
]


def extract_transactions(raw_text):
    """
    Try all known patterns and extract transactions intelligently.
    Returns a list of dicts with keys: date, description, amount, is_credit
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

    logger.warning("No matching regex patterns found for transaction extraction.")
    return []


def categorize_transaction(description):
    if not bert_model:
        logger.warning("BERT model not available, defaulting to 'Uncategorized'.")
        return "Uncategorized"

    try:
        outputs = bert_model(description[:256])
        if not outputs or not isinstance(outputs, list) or not isinstance(outputs[0], dict):
            logger.warning(f"Unexpected model output: {outputs}")
            return "Uncategorized"

        result = outputs[0]
        raw_label = result.get("label", "")
        normalized_label = raw_label.capitalize().replace("label_", "Label_")
        category = LABEL_MAP.get(normalized_label, "Uncategorized")

        logger.info(f"Categorized: '{description[:30]}...' as '{category}' (label: {normalized_label})")

        return category

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
