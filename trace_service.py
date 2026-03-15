from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


def create_tracer():
    """
    The function creates a trace exporter for OpenTelemetry.
    :return: The trace exporter.
    """
    resource = Resource.create({
        "service.name": "pet-game"
    })
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces"
    )
    span_processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    return tracer
