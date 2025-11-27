import requests
import time
from typing import Dict, Any, Optional, Tuple

class RESTClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def execute_request(
        self, endpoint: str, method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], float, int]:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        hdrs = headers or {}

        t0 = time.perf_counter()
        res = self.session.request(method, url, params=params, headers=hdrs, json=json_data, timeout=self.timeout)
        t1 = time.perf_counter()

        ms = (t1 - t0) * 1000
        size = len(res.content)

        if not res.ok:
            raise Exception("REST request failed")

        try:
            data = res.json() if res.content else {}
        except:
            data = {"raw": res.text[:120]}

        return {"code": res.status_code, "data": data}, ms, size

    def get(self, endpoint: str, params=None, headers=None):
        return self.execute_request(endpoint, "GET", params=params, headers=headers)

    def post(self, endpoint: str, params=None, headers=None, json_data=None):
        hdrs = headers or {}
        if json_data:
            hdrs["Content-Type"] = "application/json"
        return self.execute_request(endpoint, "POST", params=params, headers=hdrs, json_data=json_data)

    def close(self):
        self.session.close()