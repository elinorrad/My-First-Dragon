from typing import Tuple

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Tracer


def create_tracer() -> tuple:
    """
    The function creates a new OpenTelemetry Tracer.
    :return: The new OpenTelemetry Tracer.
    """
    # trace.set_tracer_provider(
    #     TracerProvider(
    #         resource=Resource.create({"service_name": "my-service"})
    #     )
    # )
    #
    # return trace.get_tracer(__name__)
    provider = TracerProvider(
        resource=Resource.create({"service_name": "my-service"})
    )
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__), provider


def create_jaeger_exporter() -> JaegerExporter:
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=4317
    )
    return jaeger_exporter


def create_span_processor(jaeger_exporter: JaegerExporter) -> SpanProcessor:
    span_processor = BatchSpanProcessor(jaeger_exporter)
    return span_processor
