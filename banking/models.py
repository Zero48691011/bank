from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    full_name = models.CharField("姓名", max_length=100)
    phone = models.CharField("手机号", max_length=20, blank=True)
    id_number = models.CharField("身份证号", max_length=32, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "客户"
        verbose_name_plural = "客户"

    def __str__(self) -> str:
        return self.full_name


class Account(models.Model):
    SAVINGS = "SAV"
    CHECKING = "CHK"
    ACCOUNT_TYPES = [
        (SAVINGS, "储蓄账户"),
        (CHECKING, "活期账户"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="accounts"
    )
    number = models.CharField("账号", max_length=32, unique=True)
    account_type = models.CharField(
        "账户类型", max_length=3, choices=ACCOUNT_TYPES, default=SAVINGS
    )
    balance = models.DecimalField("余额", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "账户"
        verbose_name_plural = "账户"

    def __str__(self) -> str:
        return f"{self.number} ({self.get_account_type_display()})"


class Transaction(models.Model):
    DEPOSIT = "DEP"
    WITHDRAW = "WDR"
    TRANSFER = "TRF"

    TRANSACTION_TYPES = [
        (DEPOSIT, "存款"),
        (WITHDRAW, "取款"),
        (TRANSFER, "转账"),
    ]

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    tx_type = models.CharField("交易类型", max_length=3, choices=TRANSACTION_TYPES)
    amount = models.DecimalField("金额", max_digits=12, decimal_places=2)
    created_at = models.DateTimeField("时间", auto_now_add=True)
    description = models.CharField("备注", max_length=255, blank=True)

    class Meta:
        verbose_name = "交易"
        verbose_name_plural = "交易"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_tx_type_display()} {self.amount} @ {self.created_at:%Y-%m-%d %H:%M}"


class Statement(models.Model):
    """
    账户对账单元数据（实际文件存放在 Minio 中，只在此保存对象名）。
    """

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="statements"
    )
    object_name = models.CharField("对象名", max_length=255)
    original_name = models.CharField("原文件名", max_length=255)
    uploaded_at = models.DateTimeField("上传时间", auto_now_add=True)

    class Meta:
        verbose_name = "对账单"
        verbose_name_plural = "对账单"
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return f"{self.original_name} ({self.account.number})"

