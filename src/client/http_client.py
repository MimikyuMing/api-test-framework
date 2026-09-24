import requests

from src.utils.logger import get_logger


class HttpClient:
    def __init__(self, base_url, timeout=10, retry=2):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry = retry
        self.session = requests.Session()
        self.logger = get_logger()

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        last_exc = None
        for attempt in range(self.retry + 1):
            try:
                self.logger.info(f"--> {method} {url}")
                resp = self.session.request(
                    method, url, timeout=self.timeout, **kwargs
                )
                self.logger.info(f"<-- {resp.status_code} {url}")
                if resp.status_code >= 500 and attempt < self.retry:
                    self.logger.warning(f"server error, retrying ({attempt + 1})")
                    continue
                return resp
            except requests.RequestException as e:
                last_exc = e
                self.logger.warning(f"attempt {attempt + 1} failed: {e}")
        raise last_exc
    
    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)
