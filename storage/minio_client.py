from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from django.conf import settings
from minio import Minio
from minio.error import S3Error


def get_minio_client() -> Minio:
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_USE_SSL,
    )


def ensure_bucket(client: Minio | None = None) -> None:
    client = client or get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


def upload_file(
    file_obj: BinaryIO,
    object_name: str,
    content_type: str | None = None,
) -> str:
    """
    上传文件到 Minio，返回对象名称。
    """
    client = get_minio_client()
    ensure_bucket(client)

    file_obj.seek(0, 2)
    size = file_obj.tell()
    file_obj.seek(0)

    client.put_object(
        settings.MINIO_BUCKET_NAME,
        object_name,
        file_obj,
        length=size,
        content_type=content_type,
    )
    return object_name


def upload_path_for_statement(account_number: str) -> str:
    return f"statements/{account_number}/{Path(account_number).stem}.pdf"


__all__ = ["get_minio_client", "upload_file", "upload_path_for_statement", "ensure_bucket", "S3Error"]

