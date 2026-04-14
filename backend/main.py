from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from backend.router import router
from slowapi.middleware import SlowAPIMiddleware
from backend.exception_handlers import exception_handler, rate_limit_handler
from backend.auth.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from backend.config import deployConfigs


app = FastAPI(
    debug= deployConfigs.debug_mode,
    docs_url= deployConfigs.docs_url,
    redoc_url= deployConfigs.redoc_url
)


app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins= deployConfigs.allow_origins,          # allow all frontends
    allow_credentials=False,      # IMPORTANT → no cookies, so keep False
    allow_methods= deployConfigs.allow_headers,          # allow all methods
    allow_headers= deployConfigs.allow_headers,          # allow all headers (incl. Authorization)
)

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(HTTPException, exception_handler)
app.include_router(router, prefix="/api/v1")

@app.get("/", description= "About the project", tags = ["home"])
def home():
    return {
        "info": "An initiative by ARITY- The Mathematical Society of Rajdhani College, Delhi University"
    }

@app.get("/health", description= "health check", tags= ["health"])
def health():
    return {
        "status": True
    }