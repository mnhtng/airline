import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from backend.core.config import settings
from backend.core.exception import validation_exception_handler
from backend.db.database import create_tables
from backend.routes.route import router as route_router
from backend.routes.temp_route_import import router as temp_route_router
from backend.routes.actype_seat import router as actype_seat_router
from backend.routes.temp_actype_import import router as temp_actype_router
from backend.routes.data_processing import router as data_processing_router


create_tables()

app = FastAPI(
    debug=settings.DEBUG,
    title="Airline API",
    description="API for managing airline reservations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Airline API Support",
        "url": "http://localhost:8000/docs",
        "email": "support@airlineapi.com",
    },
)

origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,  # Enable CORS
    allow_origins=origins,  # Allows requests from specified origins (domain FE)
    allow_credentials=True,  # Allows cookies to be sent
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Custom exception handler để loại bỏ "Value error, " từ Pydantic
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Include routers
api_prefix = settings.API_PREFIX

app.include_router(route_router, prefix=api_prefix)
app.include_router(temp_route_router, prefix=api_prefix)
app.include_router(actype_seat_router, prefix=api_prefix)
app.include_router(temp_actype_router, prefix=api_prefix)
app.include_router(data_processing_router, prefix=api_prefix)


# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Airline API!"}


# Start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
