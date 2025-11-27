import requests
import time
from typing import Dict, Any, Optional, Tuple

class GraphQLClient:
    def __init__(self, endpoint: str, timeout: int = 30):
        self.endpoint = endpoint
        self.timeout = timeout
        self.session = requests.Session()

    def execute_query(
        self, query: str, variables: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Tuple[Dict[str, Any], float, int]:

        body = {"query": query}
        if variables:
            body["variables"] = variables

        hdrs = headers or {}
        hdrs["Content-Type"] = "application/json"

        t0 = time.perf_counter()
        res = self.session.post(self.endpoint, json=body, headers=hdrs, timeout=self.timeout)
        t1 = time.perf_counter()

        ms = (t1 - t0) * 1000
        size = len(res.content)

        if not res.ok:
            raise Exception(f"GraphQL request failed: {res.status_code}")

        out = res.json()
        if "errors" in out:
            raise Exception("GraphQL execution error")

        data = out.get("data")
        if data is None:
            raise Exception("No data returned")

        return data, ms, size

    def close(self):
        self.session.close()