from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.routers import api_v1_router,api_healthcheck_router
from core.middlewares.catcher import CatcherExceptionsMiddleware
from core.settings import settings
from core.utils.validations import validation_pydantic_field
from core.settings.database import validate_db_conections

app = FastAPI(
    title=settings.PROJECT_NAME,
    redirect_slashes=False,
)


# Set all CORS enabled origins
app.add_middleware(CatcherExceptionsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)
app.include_router(api_healthcheck_router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

validate_db_conections()
validation_pydantic_field(app)
