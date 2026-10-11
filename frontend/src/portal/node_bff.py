import requests

from django.conf import settings


class BFF:
    def __init__(self):
        self.url = settings.NODE_URL

# ----------------------
# STATUS
# ----------------------
    def status(self, application_id):
        response = requests.get(
            f"{self.url}/services/{application_id}/status",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()
        
# ----------------------
# START
# ----------------------
    def start(self, application_id):
        response = requests.post(
            f"{self.url}/services/{application_id}/start",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

# ----------------------
# STOP
# ----------------------
    def stop(self, application_id):
        response = requests.post(
            f"{self.url}/services/{application_id}/stop",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

# ----------------------
# ACTIVE
# ----------------------
    def activate(self, application_id):
        response = requests.post(
            f"{self.url}/services/{application_id}/activate",
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

