# Statement model serializer
from rest_framework import serializers
from core.models.statement import Statement


class StatementUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ["id", "uploaded_file", "uploaded_at", "raw_text"]
        read_only_fields = ["id", "uploaded_at", "raw_text"]
