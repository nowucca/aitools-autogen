from aitools_autogen.utils import save_code_files, extract_code, clear_working_dir, summarize_files

test_response = """
This is a sample response from the API.

# filename: api/client/client.py
```python
import aiohttp
from .endpoints import DatasetEndpoint

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_datasets(self):
        async with aiohttp.ClientSession() as session:
            endpoint = DatasetEndpoint(self.base_url)
            return await endpoint.get_datasets(session)

    async def get_dataset_fields(self, dataset, version):
        async with aiohttp.ClientSession() as session:
            endpoint = DatasetEndpoint(self.base_url)
            return await endpoint.get_dataset_fields(session, dataset, version)

    async def post_dataset_records(self, dataset, version, criteria, start=0, rows=10):
        async with aiohttp.ClientSession() as session:
            endpoint = DatasetEndpoint(self.base_url)
            return await endpoint.post_dataset_records(session, dataset, version, criteria, start, rows)
```

# filename: api/client/endpoints.py
```python
import aiohttp

class DatasetEndpoint:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_datasets(self, session: aiohttp.ClientSession):
        async with session.get(f"{self.base_url}/") as response:
            return await self._handle_response(response)

    async def get_dataset_fields(self, session: aiohttp.ClientSession, dataset, version):
        async with session.get(f"{self.base_url}/{dataset}/{version}/fields") as response:
            return await self._handle_response(response)

    async def post_dataset_records(self, session: aiohttp.ClientSession, dataset, version, criteria, start, rows):
        payload = {"criteria": criteria, "start": start, "rows": rows}
        async with session.post(f"{self.base_url}/{dataset}/{version}/records", json=payload) as response:
            return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse):
        if response.status == 200:
            return await response.json()
        elif response.status == 404:
            raise Exception("Not Found")
        else:
            raise Exception(f"Unexpected status code: {response.status}")
```

This code creates an `APIClient` class that uses `aiohttp.ClientSession` to make HTTP requests to the API. The `DatasetEndpoint` class handles the specific endpoints of the API. The `_handle_response` method is used to handle the response from the API and raise exceptions for unexpected status codes.
"""


def test_extract_code():
    print(extract_code(test_response))

def test_clear_working_dir():
    clear_working_dir(".code")

def test_save_code():
    print(save_code_files(test_response, ".code"))

def test_summarize_files():
    result = summarize_files(".code")
    print(result)

