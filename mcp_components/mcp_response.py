import json


class MCPResponse:
    def __init__(self, data: dict):
        self._data = data

    def text(self) -> str:
        return json.dumps(self._data)

    def data(self) -> dict:
        return self._data
