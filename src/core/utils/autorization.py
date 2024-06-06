from fastapi import Header
from fastapi.requests import Request


def check_authorization(
    request: Request,
    X_Service_Name: str = Header(...),  # noqa: N803
    X_API_Key: str = Header(...),  # noqa: N803
):
    pass
