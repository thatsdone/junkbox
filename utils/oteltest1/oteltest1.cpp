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
 *   * continue to blush up
 *   * Write README
 *   * set attribute
 *   * use link
 */
#include <iostream>
#include <vector>
using namespace std;

#include <getopt.h>
#include "opentelemetry/sdk/version/version.h"
//OTLP/gRPC exporter
#include "opentelemetry/exporters/otlp/otlp_grpc_exporter_factory.h"
//OStream(console) exporter
#include "opentelemetry/exporters/ostream/span_exporter_factory.h"
#include "opentelemetry/sdk/trace/processor.h"
#include "opentelemetry/sdk/trace/simple_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"
#include "opentelemetry/trace/provider.h"
#include "opentelemetry/sdk/trace/processor.h"
#include "opentelemetry/sdk/resource/resource.h"
#include "opentelemetry/trace/span_startoptions.h"
#include "opentelemetry/trace/context.h"
namespace trace     = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace otlp = opentelemetry::exporter::otlp;
namespace trace_exporter = opentelemetry::exporter::trace;
namespace resource_sdk  = opentelemetry::sdk::resource;

int main(int argc, char **argv)
{
    std::string endpoint = "localhost:4317";
    std::string service_name = "oteltest1";
    bool console_processor = false;
    bool otlp_processor = false;

    const option longopts[] = {
      {"endpoint", required_argument, nullptr  , 'e'},
      {"service_name", required_argument, nullptr, 'S'},
      {"console", optional_argument, nullptr, 'C'},
      {"otlp", optional_argument, nullptr, 'o'}
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
      case 'C':
	console_processor = true;
      case 'o':
	otlp_processor = true;
      }
    }

    std::vector<std::unique_ptr<trace_sdk::SpanProcessor>> processors;

    if (console_processor) {
      auto exporter = trace_exporter::OStreamSpanExporterFactory::Create();
      auto processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
      processors.push_back(std::move(processor));
    }
    if (otlp_processor) {
      otlp::OtlpGrpcExporterOptions opts;
      opts.use_ssl_credentials = false;
      opts.endpoint = std::move(endpoint);
      auto exporter  = otlp::OtlpGrpcExporterFactory::Create(opts);
      auto processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
      processors.push_back(std::move(processor));
    }

    auto resource_attributes = resource_sdk::ResourceAttributes
      {
        {"service.name", std::move(service_name)}
      };
    auto resource = resource_sdk::Resource::Create(resource_attributes);

    std::shared_ptr<trace::TracerProvider> provider =
      trace_sdk::TracerProviderFactory::Create(std::move(processors),
					       resource);
    //TODO(thatsdone): create NULL provider and use AddProcessor()s

    trace::Provider::SetTracerProvider(provider);
    auto tracer = provider->GetTracer("otetest1", OPENTELEMETRY_SDK_VERSION);
    //
    //main span
    auto span_main = tracer->StartSpan("main");
    cout << "span_main" << endl;
    span_main->SetAttribute("attribute_key1", "attribute_value1");

    //child span
    //do context propagation
    trace::StartSpanOptions options;
    options.parent = span_main->GetContext();
    auto span_child1 = tracer->StartSpan("child1", options);
    span_child1->SetAttribute("attribute_key2", "attribute_value2");

    cout << "span_child1" << endl;

    //AddLink : Looks like AddLink requires ABI V2
    //auto span_child2 = tracer->StartSpan("child2");
    //span_child2.AddLink(span_main->GetContext(), nullptr);

    span_child1->End();
    //child span: end

    span_main->End();
    //main span: end

    return 0;
}
