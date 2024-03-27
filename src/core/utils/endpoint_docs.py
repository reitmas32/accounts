class EndpointDoc:
    def __init__(self, summary="", description="", responses=None):
        self._summary = summary
        self._description = description
        self._responses = responses or {}

    def as_dict(self):
        return {
            "summary": self._summary,
            "description": self._description,
            "responses": self._responses,
        }
