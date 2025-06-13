# App-specific routes
from django.urls import path
from core.views.auth_views import RegisterView, LoginView
from core.views.insight_views import UserTransactionListView
from core.views.upload_views import StatementUploadView
from core.views.upload_views import ReprocessStatementView
from core.views.insight_views import FinancialInsightsView

from core.views.insight_views import ExportAllTransactionsCSV
from core.views.upload_views import ExportStatementZIP
urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("upload/statement/", StatementUploadView.as_view(), name="upload_statement"),
    path("insights/", FinancialInsightsView.as_view(), name="financial_insights"),
    path("transactions/", UserTransactionListView.as_view(), name="user_transactions"),
    path("reprocess_statement/<int:statement_id>/", ReprocessStatementView.as_view(), name="reprocess_statement"),
    path("download/transactions/", ExportAllTransactionsCSV.as_view(), name="export_all_csv"),
    path("download/statement/<int:statement_id>/", ExportStatementZIP.as_view(), name="export_statement_zip"),
]
