from logging import Filter
from logging import INFO

from loguru import logger
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import SERVICE_NAME

resource = Resource({SERVICE_NAME: "LogAPP"})
provider = LoggerProvider(resource=resource)
processor = BatchLogRecordProcessor(
    OTLPLogExporter(endpoint="https://collector.your_domain.dev" + "/v1/logs")
)
provider.add_log_record_processor(processor)

set_logger_provider(provider)


class RemoveExtra(Filter):
    def filter(self, record):
        del record.extra
        return True


handler = LoggingHandler(level=INFO, logger_provider=provider)
handler.addFilter(RemoveExtra())

# OTel Handler
logger.add(handler, level="DEBUG", serialize=True)


for i in range(100):
    from time import sleep

    sleep(1)
    logger.critical("aaaaaaaa")
    logger.info("aaaaaaaa")

# @logger.catch
# def xpto():
#     1/0


# xpto()
