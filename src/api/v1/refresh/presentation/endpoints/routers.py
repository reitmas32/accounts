from fastapi import APIRouter

router = APIRouter(prefix="/refresh-token", tags=["CRUD refresh-token"])

router_operations = APIRouter(tags=["API Auth"])

