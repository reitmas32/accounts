from fastapi import APIRouter

router_crud = APIRouter(prefix="/emails", tags=["CRUD emails"])

router_operations = APIRouter(prefix="/emails", tags=["API Auth"])

