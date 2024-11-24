from fastapi import APIRouter

router_crud = APIRouter(prefix="/login_methods", tags=["CRUD login_methods"])

router_verify = APIRouter(tags=["API Auth"])

