# cli/invarum/client.py
import os
import requests
import time
from typing import Dict, Any

# Default to localhost for now, but ready for prod
DEFAULT_API_BASE = "https://api.invarum.com"

class InvarumClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = os.getenv("INVARUM_API_BASE", DEFAULT_API_BASE)
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def submit_run(self, prompt: str, task: str) -> str:
        """Submits a run and returns the run_id"""
        url = f"{self.base_url}/runs"
        try:
            resp = requests.post(
                url, 
                json={"prompt": prompt, "task": task}, 
                headers=self.headers
            )
            resp.raise_for_status()
            return resp.json()["run_id"]
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                #print("error is: ", e)
                raise ValueError("Invalid API Key")
            raise e

    def get_run(self, run_id: str) -> Dict[str, Any]:
        """Fetches run details"""
        url = f"{self.base_url}/runs/{run_id}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def wait_for_run(self, run_id: str, poll_interval=2) -> Dict[str, Any]:
        """Polls until run is complete"""
        while True:
            data = self.get_run(run_id)
            status = data.get("status")
            
            if status == "succeeded":
                return data
            if status == "failed":
                raise RuntimeError(f"Run failed: {data.get('error')}")
            
            time.sleep(poll_interval)