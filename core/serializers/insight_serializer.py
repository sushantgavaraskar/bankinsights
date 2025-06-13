# Insight model serializer
from rest_framework import serializers

class CategoryBreakdownSerializer(serializers.Serializer):
    category = serializers.CharField()
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)

class MonthlyTrendSerializer(serializers.Serializer):
    month = serializers.CharField()
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)

class TopMerchantSerializer(serializers.Serializer):
    merchant = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class RecurringExpenseSerializer(serializers.Serializer):
    description = serializers.CharField()
    monthly_average = serializers.DecimalField(max_digits=12, decimal_places=2)

class SmartSuggestionSerializer(serializers.Serializer):
    suggestion = serializers.CharField()
