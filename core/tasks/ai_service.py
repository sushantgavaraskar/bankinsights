# core/tasks/ai_service.py
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class TransactionCategorizer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = pipeline(
                    "text-classification",
                    model="kuro-08/bert-transaction-categorization",
                    tokenizer="kuro-08/bert-transaction-categorization"
                )
            except Exception as e:
                logger.warning(f"BERT model load failed: {e}")
                cls._instance = None
        return cls._instance
