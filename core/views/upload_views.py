from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status, permissions
from django.http import HttpResponse
import logging

from core.serializers.statement_serializer import StatementUploadSerializer
from core.tasks.ocr import extract_text_from_pdf
from core.tasks.preprocess import process_and_store_transactions
from core.models.statement import Statement
from core.models.transaction import Transaction

logger = logging.getLogger(__name__)

class StatementUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = StatementUploadSerializer(data=request.data)
        if serializer.is_valid():
            statement = serializer.save(user=request.user)
            try:
                file_path = statement.uploaded_file.path
                raw_text = extract_text_from_pdf(file_path)
                statement.raw_text = raw_text
                statement.save()

                txn_count = process_and_store_transactions(user=request.user, statement=statement)
                logger.info(f"Uploaded and processed {txn_count} transactions for user {request.user.email}")
                return Response({
                    "message": "PDF uploaded and processed successfully.",
                    "statement_id": statement.id,
                    "raw_text_snippet": raw_text[:300] + "..." if raw_text else "",
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Statement processing failed: {e}")
                return Response({"error": "Failed to process statement."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning(f"Invalid statement upload: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReprocessStatementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, statement_id):
        try:
            statement = Statement.objects.get(id=statement_id, user=request.user)
        except Statement.DoesNotExist:
            return Response({"error": "Statement not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Delete old transactions
            Transaction.objects.filter(statement=statement).delete()

            file_path = statement.uploaded_file.path
            raw_text = extract_text_from_pdf(file_path)
            statement.raw_text = raw_text
            statement.save()

            txn_count = process_and_store_transactions(request.user, statement)
            logger.info(f"Reprocessed statement {statement_id} with {txn_count} transactions for user {request.user.email}")
            return Response({"message": f"Reprocessed successfully. {txn_count} transactions added."})
        except Exception as e:
            logger.error(f"Reprocessing failed: {e}")
            return Response({"error": "Failed to reprocess statement."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import csv, zipfile
from io import BytesIO, StringIO
from django.http import HttpResponse
from core.models.transaction import Transaction, Statement
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ExportStatementZIP(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, statement_id):
        try:
            statement = Statement.objects.get(id=statement_id, user=request.user)
        except Statement.DoesNotExist:
            return HttpResponse("Statement not found.", status=404)

        transactions = Transaction.objects.filter(statement=statement)

        # Create in-memory ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # 1. CSV File
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(['Date', 'Description', 'Amount', 'Category', 'Credit/Debit'])

            for txn in transactions:
                writer.writerow([
                    txn.date.strftime('%Y-%m-%d'),
                    txn.description,
                    txn.amount,
                    txn.category,
                    'Credit' if txn.is_credit else 'Debit'
                ])

            zip_file.writestr("transactions.csv", csv_buffer.getvalue())

            # 2. OCR Text
            zip_file.writestr("raw_ocr.txt", statement.raw_text or "No text extracted.")

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename=statement_{statement.id}.zip'
        return response
