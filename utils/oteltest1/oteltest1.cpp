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
 * TODO:
 *   * Blushup
 *   * Write README
 */
#include <iostream>
using namespace std;

#include <getopt.h>
#include "opentelemetry/sdk/version/version.h"
#include "opentelemetry/exporters/otlp/otlp_grpc_exporter_factory.h"
#include "opentelemetry/sdk/trace/processor.h"
#include "opentelemetry/sdk/trace/simple_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"
#include "opentelemetry/trace/provider.h"
#include "opentelemetry/sdk/resource/resource.h"
#include "opentelemetry/trace/span_startoptions.h"
#include "opentelemetry/trace/context.h"
namespace trace     = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace otlp = opentelemetry::exporter::otlp;
namespace resource_sdk  = opentelemetry::sdk::resource;

int main(int argc, char **argv)
{
    std::string endpoint = "localhost:4317";
    std::string service_name = "oteltest1";

    const option longopts[] = {
      {"endpoint", required_argument, nullptr  , 'e'},
      {"service_name", required_argument, nullptr, 'S'}
    };

    while (1) {
      const int opt = getopt_long(argc, argv, "e:S:", longopts, 0);
      if (opt < 0) {
	break;
      }
      switch (opt) {
      case 'e':
	endpoint = std::string(optarg);
      case 'S':
	service_name = std::string(optarg);
      }
    }

    otlp::OtlpGrpcExporterOptions opts;
    opts.use_ssl_credentials = false;
    opts.endpoint = std::move(endpoint);
    auto exporter  = otlp::OtlpGrpcExporterFactory::Create(opts);
    auto processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
    auto resource_attributes = resource_sdk::ResourceAttributes
      {
        {"service.name", std::move(service_name)}
      };
    auto resource = resource_sdk::Resource::Create(resource_attributes);
    auto received_attributes = resource.GetAttributes();

    std::shared_ptr<trace::TracerProvider> provider =
      trace_sdk::TracerProviderFactory::Create(std::move(processor),
					       resource);
    trace::Provider::SetTracerProvider(provider);
    auto tracer = provider->GetTracer("otetest1", OPENTELEMETRY_SDK_VERSION);
    auto span_main = tracer->StartSpan("main");
    cout << "span_main" << endl;

    trace::StartSpanOptions options;
    options.parent = span_main->GetContext();
    auto span_child1 = tracer->StartSpan("child1", options);

    cout << "span_child1" << endl;

    return 0;
}


