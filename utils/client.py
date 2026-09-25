import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class APIClient:
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        # Retry on transient 5xx and connection errors — keeps CI green
        retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path, **kwargs) -> requests.models.Response:
        return self.session.get(self._url(path), **kwargs)

    def post(self, path, **kwargs) -> requests.models.Response:
        return self.session.post(self._url(path), **kwargs)

    def put(self, path, **kwargs) -> requests.models.Response:
        return self.session.put(self._url(path), **kwargs)

    def delete(self, path, **kwargs) -> requests.models.Response:
        return self.session.delete(self._url(path), **kwargs)
