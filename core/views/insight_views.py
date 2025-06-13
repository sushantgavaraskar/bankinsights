# insightsview.py

from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
import csv, logging
from io import StringIO
from core.models.transaction import Transaction
from core.serializers.transaction_serializer import TransactionSerializer
from core.tasks.ai_utils import (
    get_categorized_expense_breakdown,
    get_monthly_trends,
    get_top_merchants,
    get_recurring_expenses,
    get_savings_insights,
)

logger = logging.getLogger(__name__)

class FinancialInsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            data = {
                "categorized_expenses": get_categorized_expense_breakdown(user),
                "monthly_trends": get_monthly_trends(user),
                "top_merchants": get_top_merchants(user),
                "recurring_expenses": get_recurring_expenses(user),
                "savings_summary": get_savings_insights(user)
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Insight generation failed: {e}")
            return Response({"error": "Failed to generate insights"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'is_credit']
    search_fields = ['description']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        user = self.request.user
        month = self.request.query_params.get('month')
        queryset = Transaction.objects.filter(user=user)

        if month:
            try:
                year, month = map(int, month.split('-'))
                queryset = queryset.filter(date__year=year, date__month=month)
            except ValueError:
                logger.warning("Invalid month format")
        return queryset


class ExportAllTransactionsCSV(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            transactions = Transaction.objects.filter(user=user)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="all_transactions.csv"'

            writer = csv.writer(response)
            writer.writerow(['Date', 'Description', 'Amount', 'Category', 'Credit/Debit'])

            for txn in transactions:
                writer.writerow([
                    txn.date.strftime('%Y-%m-%d'),
                    txn.description,
                    txn.amount,
                    txn.category,
                    'Credit' if txn.is_credit else 'Debit'
                ])
            return response
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            return Response({"error": "Failed to export CSV"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

