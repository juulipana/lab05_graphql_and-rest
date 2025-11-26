import requests
import time
from typing import Dict, Any, Optional, Tuple


class RESTClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def execute_request(self, endpoint: str, method: str = 'GET', 
                       params: Optional[Dict[str, Any]] = None,
                       headers: Optional[Dict[str, str]] = None,
                       json_data: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], float, int]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        start_time = time.perf_counter()
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            end_time = time.perf_counter()
            response_time_ms = (end_time - start_time) * 1000
            response_size_bytes = len(response.content)
            
            try:
                data = response.json() if response.content else {}
            except ValueError:
                data = {'raw_content': response.text[:100]}
            
            result = {
                'status_code': response.status_code,
                'data': data
            }
            
            return result, response_time_ms, response_size_bytes
            
        except requests.exceptions.RequestException as e:
            end_time = time.perf_counter()
            response_time_ms = (end_time - start_time) * 1000
            raise Exception(f"REST request failed: {str(e)}") from e
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, Any], float, int]:
        return self.execute_request(endpoint, method='GET', params=params, headers=headers)
    
    def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None,
             json_data: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], float, int]:
        if json_data:
            if headers is None:
                headers = {}
            headers['Content-Type'] = 'application/json'
            return self.execute_request(endpoint, method='POST', params=params, 
                                       headers=headers, json_data=json_data)
        return self.execute_request(endpoint, method='POST', params=params, headers=headers)
    
    def close(self):
        self.session.close()

