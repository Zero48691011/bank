from __future__ import annotations

from django import forms

from .models import Account, Statement, Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["account", "tx_type", "amount", "description"]


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["customer", "number", "account_type"]


class StatementUploadForm(forms.Form):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        label="账户",
    )
    file = forms.FileField(label="对账单文件")

