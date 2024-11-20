from fastapi import APIRouter

router = APIRouter(prefix="/platforms", tags=["CRUD platforms"])

router_operations = APIRouter(prefix="/platforms", tags=["API Auth"])
