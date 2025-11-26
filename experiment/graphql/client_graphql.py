import requests
import time
import json
from typing import Dict, Any, Optional, Tuple


class GraphQLClient:
    def __init__(self, endpoint: str, timeout: int = 30):
        self.endpoint = endpoint
        self.timeout = timeout
        self.session = requests.Session()
    
    def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Tuple[Dict[str, Any], float, int]:
        payload = {
            'query': query
        }
        
        if variables:
            payload['variables'] = variables
        
        if headers is None:
            headers = {}
        
        headers.setdefault('Content-Type', 'application/json')
        
        start_time = time.perf_counter()
        
        try:
            response = self.session.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            end_time = time.perf_counter()
            response_time_ms = (end_time - start_time) * 1000
            response_size_bytes = len(response.content)
            
            result = response.json()
            
            if 'errors' in result:
                raise Exception(f"GraphQL errors: {result['errors']}")
            
            return result, response_time_ms, response_size_bytes
            
        except requests.exceptions.RequestException as e:
            end_time = time.perf_counter()
            response_time_ms = (end_time - start_time) * 1000
            raise Exception(f"GraphQL request failed: {str(e)}") from e
    
    def close(self):
        self.session.close()

