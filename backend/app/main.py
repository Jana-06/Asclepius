"""
SwasthyaFlow AI - FastAPI Backend Application
AI-powered public healthcare triage and hospital load optimization system
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
import time

from app.core.config import settings
from app.api.v1 import triage, hospitals, outbreak, admin, patients, tokens
from app.core.database import engine, Base

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting SwasthyaFlow AI Backend", version=settings.VERSION)

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Load ML models
    from app.services.triage_engine import triage_engine
    await triage_engine.load_models()

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down SwasthyaFlow AI Backend")
    await engine.dispose()


app = FastAPI(
    title="SwasthyaFlow AI",
    description="AI-powered public healthcare triage and hospital load optimization system",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__}
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": "SwasthyaFlow AI"
    }


# API Routers
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(triage.router, prefix="/api/v1/triage", tags=["Triage"])
app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["Hospitals"])
app.include_router(outbreak.router, prefix="/api/v1/outbreak", tags=["Outbreak Detection"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(tokens.router, prefix="/api/v1/tokens", tags=["Tokens"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to SwasthyaFlow AI",
        "description": "AI-powered public healthcare triage and hospital load optimization",
        "docs": "/docs",
        "health": "/health"
    }

