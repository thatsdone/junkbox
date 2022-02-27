package com.github.thatsdone.junkbox;

import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.context.Context;
import io.opentelemetry.context.propagation.TextMapGetter;
import io.opentelemetry.context.propagation.TextMapSetter;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;
import io.opentelemetry.exporter.otlp.http.trace.OtlpHttpSpanExporter;
import io.opentelemetry.api.trace.propagation.W3CTraceContextPropagator;
import io.opentelemetry.api.trace.SpanContext;
import io.opentelemetry.api.trace.TraceFlags;
import io.opentelemetry.api.trace.TraceState;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
        String serviceName = null;
        String endpoint = null;
        //      Tracer tracer = null;

        Resource resource = Resource.getDefault().toBuilder()
            .put("service.name", serviceName).build();

        // can be  OtlpHttpSpanExporter but endpoint should be
        // 'http://localhost:4318/api/v1/traces' for example.
        // not just'http://localhost:4317/' for gRPC case.
        // Also, Class JaegerThriftSpanExporter is available.
        SdkTracerProvider sdkTracerProvider =
            SdkTracerProvider.builder()
            .addSpanProcessor(BatchSpanProcessor
                              .builder(OtlpGrpcSpanExporter.builder()
                                       .setEndpoint(endpoint)
                                       .build())
                              .build())
            .setResource(resource)
            .build();

        OpenTelemetrySdk openTelemetry =
            OpenTelemetrySdk.builder()
            .setTracerProvider(sdkTracerProvider)
            .buildAndRegisterGlobal();
        Tracer tracer = openTelemetry.getTracer("myapp");
        W3CTraceContextPropagator otlpPropagator =
            W3CTraceContextPropagator.getInstance();
    }

    public static Span startSpan(Context context, String spanName, Tracer tracer) {
        if (context == null) {
            return tracer.spanBuilder(spanName).setParent(Context.current()).startSpan();
        } else {
            return tracer.spanBuilder(spanName).setParent(context).startSpan();
        }
    }
}
