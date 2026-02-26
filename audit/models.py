from __future__ import annotations

from django.db import models


class AuditLog(models.Model):
    """
    存储在 MongoDB 中的审计日志，用于记录关键操作。
    """

    action = models.CharField("操作", max_length=100)
    actor = models.CharField("操作者", max_length=100, blank=True)
    data = models.JSONField("数据", blank=True, null=True)
    created_at = models.DateTimeField("时间", auto_now_add=True)

    class Meta:
        app_label = "audit"
        verbose_name = "审计日志"
        verbose_name_plural = "审计日志"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action} @ {self.created_at:%Y-%m-%d %H:%M}"

