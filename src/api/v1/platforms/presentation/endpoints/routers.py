from fastapi import APIRouter

router_crud = APIRouter(prefix="/platforms", tags=["CRUD platforms"])

router_operations = APIRouter(prefix="/platforms", tags=["API Auth"])
