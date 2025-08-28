from app.router.app_routes import router as app_router
from app.router.v1 import routers
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.trace import get_current_span
from opentelemetry.trace.span import Span


def add_trace_id_header(response: Response):
    span: Span = get_current_span()
    trace_id = span.get_span_context().trace_id

    trace_id_hex = format(trace_id, "032x")
    response.headers["otel-trace-id"] = trace_id_hex


app = FastAPI(
    dependencies=[Depends(add_trace_id_header)],
    title="Password Generator",
    version="1.0.0",
    description="Password api to generate random pins and passwords with cicd pipe, test hadson",
    contact={
        "name": "GabrielCarvalho",
        "email": "gabrielcarvalho.workk@gmail.com",
        "url": "https://www.linkedin.com/in/gabzsz",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Liberar para todos os domínios (ajuste conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=routers)
app.include_router(router=app_router)
