from collections import defaultdict
from datetime import datetime
from core.models.transaction import Transaction
import logging

logger = logging.getLogger(__name__)

STOP_WORDS = {"amazon", "services", "payment", "debit", "upi", "account"}

def get_categorized_expense_breakdown(user):
    result = defaultdict(float)
    for txn in Transaction.objects.filter(user=user, is_credit=False):
        result[txn.category] += float(txn.amount)
    return dict(result)

def get_monthly_trends(user):
    trends = defaultdict(float)
    for txn in Transaction.objects.filter(user=user, is_credit=False):
        key = txn.date.strftime("%Y-%m")
        trends[key] += float(txn.amount)
    return dict(trends)

def get_top_merchants(user, top_n=5):
    merchant_count = defaultdict(int)
    for txn in Transaction.objects.filter(user=user):
        words = txn.description.lower().split()
        for w in words:
            if w.isalpha() and len(w) > 3 and w not in STOP_WORDS:
                merchant_count[w] += 1
    sorted_merchants = sorted(merchant_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_merchants[:top_n]

def get_recurring_expenses(user):
    raw_txns = Transaction.objects.filter(user=user, is_credit=False)
    grouped = defaultdict(list)
    for txn in raw_txns:
        grouped[txn.description.lower()].append(float(txn.amount))

    recurring = {}
    for desc, amounts in grouped.items():
        if len(amounts) >= 3:
            avg_amt = sum(amounts) / len(amounts)
            recurring[desc] = round(avg_amt, 2)

    return recurring

def get_savings_insights(user):
    credits = sum(txn.amount for txn in Transaction.objects.filter(user=user, is_credit=True))
    debits = sum(txn.amount for txn in Transaction.objects.filter(user=user, is_credit=False))
    savings = credits - debits
    return {
        "total_income": round(credits, 2),
        "total_expenses": round(debits, 2),
        "estimated_savings": round(savings, 2),
        "suggestion": "Reduce dining or subscriptions if low on savings." if savings < (0.1 * credits) else "You're saving well!"
    }
