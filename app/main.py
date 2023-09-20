from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
print(settings.BACKEND_CORS_ORIGINS)
if settings.BACKEND_CORS_ORIGINS:
    cleaned_origins = [str(origin).rstrip('/') for origin in settings.BACKEND_CORS_ORIGINS] # Remove the trailing slash that Pydantic adds
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cleaned_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
