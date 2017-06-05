from __future__ import unicode_literals

from django.apps import AppConfig


class BindConfig(AppConfig):
    name = 'bind'

    def ready(self):
        import bind.signals