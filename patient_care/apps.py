from django.apps import AppConfig


class PatientCareConfig(AppConfig):
    name = 'patient_care'

    def ready(self):
        import patient_care.signals