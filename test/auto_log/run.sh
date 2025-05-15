export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_EXPORTER_OTLP_ENDPOINT=https://collector.your_domain.dev
export OTEL_EXPORTER_OTLP_INSECURE=true
export OTEL_LOGS_EXPORTER=otlp
export OTEL_SERVICE_NAME=sample

# pip install opentelemetry-distro
# pip install opentelemetry-exporter-grpc

# opentelemetry-bootstrap -a install

opentelemetry-instrument python exemplo_01.py
