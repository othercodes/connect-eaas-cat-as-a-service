import pkg_resources
import toml

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, sampling, Tracer, SpanProcessor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor


class Observer:
    def __init__(self, ot_tracer: Tracer):
        self._ot_tracer = ot_tracer

    @property
    def tracer(self) -> Tracer:
        return self._ot_tracer


def provide_ot_span_exporter(self, telemetry_endpoint: str, telemetry_auth_token: str) -> SpanExporter:
    return OTLPSpanExporter(
        endpoint=telemetry_endpoint,
        headers={
            "Authorization": telemetry_auth_token
        },
    )


def provide_ot_span_processor(self, ot_span_exporter: SpanExporter) -> SpanProcessor:
    return BatchSpanProcessor(ot_span_exporter)


def provide_ot_tracer(self, ot_span_processor: SpanProcessor, extension_name: str) -> Tracer:
    tracer_provider = TracerProvider(
        sampler=sampling.ALWAYS_ON,
        resource=Resource.create({
            "service.name": extension_name,
            "service.version": pkg_resources.get_distribution(extension_name).version,
            "connect.extension-runner": pkg_resources.get_distribution("connect-extension-runner").version,
            "connect.openapi-client": pkg_resources.get_distribution("connect-openapi-client").version,
        })
    )

    tracer_provider.add_span_processor(ot_span_processor)

    trace.set_tracer_provider(tracer_provider)
    return trace.get_tracer('DevOpsConnectorInstrumentor')


def provide_ot_observer(self, ot_tracer: Tracer) -> Observer:
    # automatic instrumentation of requests library
    RequestsInstrumentor().instrument()

    return Observer(ot_tracer)
