from django.urls import path

from . import views

app_name = "banking"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("transactions/new/", views.create_transaction, name="transaction_new"),
    path(
        "accounts/<int:account_id>/transactions/new/",
        views.create_transaction,
        name="transaction_new_for_account",
    ),
    path(
        "accounts/<int:account_id>/statements/upload/",
        views.upload_statement,
        name="statement_upload_for_account",
    ),
    path("statements/upload/", views.upload_statement, name="statement_upload"),
]

