from fastapi import Query


class PaginationParams:
    """Dependency for extracting pagination query parameters."""

    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    ):
        self.skip = skip
        self.limit = limit


def create_response(data, message: str = "Success", meta: dict | None = None) -> dict:
    """Wrap any payload in a standard API response envelope."""
    response: dict = {"message": message, "data": data}
    if meta is not None:
        response["meta"] = meta
    return response
