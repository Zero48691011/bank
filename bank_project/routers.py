from __future__ import annotations


class BankRouter:
    """
    将审计相关的模型路由到 MongoDB，其余使用默认 MySQL。
    约定：app_label 为 'audit' 的模型走 mongo，其余走 default。
    """

    mongo_app_labels = {"audit"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.mongo_app_labels:
            return "mongo"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.mongo_app_labels:
            return "mongo"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.mongo_app_labels
            or obj2._meta.app_label in self.mongo_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.mongo_app_labels:
            return db == "mongo"
        return db == "default"

