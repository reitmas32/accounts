from fastapi import APIRouter

router = APIRouter(prefix="/codes", tags=["CRUD codes"])

router_operations = APIRouter(prefix="/codes", tags=["API Auth"])
