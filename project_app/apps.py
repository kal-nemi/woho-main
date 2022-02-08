from django.apps import AppConfig


class Project_AppConfig(AppConfig):
    name = 'project_app'

    def ready(self):
        import project_app.signals
