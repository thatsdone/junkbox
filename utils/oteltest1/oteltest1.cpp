/**
 * oteltest1.cpp: A tiny exercise program for OpenTelemetry C++
 *
 * License:
 *   Apache License, Version 2.0
 * History:
 * 2024/01/08 v0.1 Initial version
 * Author:
 *   Masanori Itoh <masanori.itoh@gmail.com>
 * REFERENCES:
 *   * https://opentelemetry.io/docs/instrumentation/cpp/exporters/
 * NOTES:
 *  How to build.
 *    `g++  oteltest1.cpp -lopentelemetry_exporter_otlp_grpc -lopentelemetry_trace *  -o oteltest1`
 * TODO:
 *   * Blushup
 *   * Write README
 */
#include <iostream>
using namespace std;

#include "opentelemetry/exporters/otlp/otlp_grpc_exporter_factory.h"
#include "opentelemetry/sdk/trace/processor.h"
#include "opentelemetry/sdk/trace/simple_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"
#include "opentelemetry/trace/provider.h"

namespace trace     = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace otlp = opentelemetry::exporter::otlp;

int main()
{
    opentelemetry::exporter::otlp::OtlpGrpcExporterOptions opts;

    opts.use_ssl_credentials = false;
    opts.endpoint = "localhost:4317";

    auto exporter  = otlp::OtlpGrpcExporterFactory::Create(opts);
    auto processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
    std::shared_ptr<opentelemetry::trace::TracerProvider> provider =
      trace_sdk::TracerProviderFactory::Create(std::move(processor));
    trace::Provider::SetTracerProvider(provider);
    auto tracer = provider->GetTracer("otetest1", "1.0.0");
    auto span = tracer->StartSpan("main");

    cout << "Hello World";

    return 0;
}


