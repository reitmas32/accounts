from fastapi import APIRouter

router_crud = APIRouter(prefix="/refresh-token", tags=["CRUD refresh-token"])

router_operations = APIRouter(tags=["API Auth"])

