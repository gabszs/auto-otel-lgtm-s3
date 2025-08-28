from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configurar o recurso com o nome do serviço
resource = Resource(attributes={SERVICE_NAME: "test-service"})

# Configurar o provedor de tracer com o recurso
provider = TracerProvider(resource=resource)

# Criar um exportador OTLP apontando para o seu coletor
otlp_exporter = OTLPSpanExporter(endpoint="https://collector.your_domain.dev/v1/traces")

# Adicionar o exportador ao provedor
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)

# Definir o provedor global
trace.set_tracer_provider(provider)

# Obter um tracer
tracer = trace.get_tracer(__name__)

# Criar um span para teste
for i in range(100000):
    from time import sleep

    sleep(1)
    with tracer.start_as_current_span("test-span"):
        print("Enviando span de teste para o coletor")

    # Forçar a exportação de spans pendentes
    provider.force_flush()
