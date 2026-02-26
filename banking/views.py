from __future__ import annotations

from decimal import Decimal

from django.contrib import messages
from django.db import transaction as db_transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from audit.models import AuditLog
from storage.minio_client import upload_file
from .forms import StatementUploadForm, TransactionForm
from .models import Account, Statement


def dashboard(request: HttpRequest) -> HttpResponse:
    accounts = Account.objects.select_related("customer").all().order_by("number")
    return render(
        request,
        "banking/dashboard.html",
        {
            "accounts": accounts,
        },
    )


@db_transaction.atomic
def create_transaction(request: HttpRequest, account_id: int | None = None) -> HttpResponse:
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            account = tx.account
            amount: Decimal = tx.amount
            if tx.tx_type == tx.DEPOSIT:
                account.balance += amount
            elif tx.tx_type in (tx.WITHDRAW, tx.TRANSFER):
                if account.balance < amount:
                    messages.error(request, "余额不足，无法完成交易。")
                    return redirect(reverse("banking:dashboard"))
                account.balance -= amount
            account.save()
            tx.save()
            # 写入 MongoDB 审计日志
            AuditLog.objects.create(
                action="transaction_created",
                actor=request.user.username if request.user.is_authenticated else "",
                data={
                    "account": account.number,
                    "tx_type": tx.tx_type,
                    "amount": float(amount),
                    "description": tx.description,
                },
            )
            messages.success(request, "交易已记录。")
            return redirect(reverse("banking:dashboard"))
    else:
        initial = {}
        if account_id is not None:
            account = get_object_or_404(Account, pk=account_id)
            initial["account"] = account
        form = TransactionForm(initial=initial)

    return render(
        request,
        "banking/transaction_form.html",
        {"form": form},
    )


def upload_statement(request: HttpRequest, account_id: int | None = None) -> HttpResponse:
    if request.method == "POST":
        form = StatementUploadForm(request.POST, request.FILES)
        if form.is_valid():
            account = form.cleaned_data["account"]
            file = form.cleaned_data["file"]
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            object_name = f"statements/{account.number}/{timestamp}_{file.name}"

            upload_file(file, object_name, getattr(file, "content_type", None))

            Statement.objects.create(
                account=account,
                object_name=object_name,
                original_name=file.name,
            )

            AuditLog.objects.create(
                action="statement_uploaded",
                actor=request.user.username if request.user.is_authenticated else "",
                data={
                    "account": account.number,
                    "object_name": object_name,
                    "original_name": file.name,
                },
            )

            messages.success(request, "对账单已上传。")
            return redirect(reverse("banking:dashboard"))
    else:
        initial = {}
        if account_id is not None:
            account = get_object_or_404(Account, pk=account_id)
            initial["account"] = account
        form = StatementUploadForm(initial=initial)

    return render(
        request,
        "banking/statement_upload_form.html",
        {
            "form": form,
        },
    )

