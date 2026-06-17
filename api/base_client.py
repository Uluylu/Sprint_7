import data.urls


class BaseClient:
    def __init__(self):
        self.base_url = data.urls.BASE_URL
        self.headers = {"Content-Type": "application/json"}
        