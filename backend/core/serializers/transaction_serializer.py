# Transaction model serializer
from rest_framework import serializers
from core.models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]
