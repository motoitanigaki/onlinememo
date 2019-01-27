from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "onlinememo2"

    def ready(self):
        import_module("onlinememo2.receivers")
