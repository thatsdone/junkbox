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
#include "opentelemetry/sdk/trace/batch_span_processor_factory.h"
#include "opentelemetry/sdk/trace/batch_span_processor_options.h"
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
namespace common  = opentelemetry::common;

int main(int argc, char **argv)
{
    std::string endpoint = "localhost:4317";
    std::string service_name = "oteltest1";
    bool console_exporter = false;
    bool otlp_exporter = false;
    bool batch_processor = false;

    const option longopts[] = {
      {"endpoint", required_argument, nullptr  , 'e'},
      {"service_name", required_argument, nullptr, 'S'},
      {"console", optional_argument, nullptr, 'C'},
      {"otlp", optional_argument, nullptr, 'o'},
      {"batch", optional_argument, nullptr, 'B'}
    };

    while (1) {
      const int opt = getopt_long(argc, argv, "e:S:CoB", longopts, 0);
      if (opt < 0) {
        break;
      }
      switch (opt) {
      case 'e':
        endpoint = std::string(optarg);
        break;
      case 'S':
        service_name = std::string(optarg);
        break;
      case 'C':
        console_exporter = true;
        break;
      case 'o':
        otlp_exporter = true;
        break;
      case 'B':
        batch_processor = true;
        break;
      }
    }

    std::vector<std::unique_ptr<trace_sdk::SpanProcessor>> processors;

    if (console_exporter) {
      auto os_exporter = trace_exporter::OStreamSpanExporterFactory::Create();
      if (batch_processor) {
        trace_sdk::BatchSpanProcessorOptions options{};
        options.max_queue_size = 25;
        options.schedule_delay_millis = std::chrono::milliseconds(5000);
        options.max_export_batch_size = 10;
        auto batch_processor = trace_sdk::BatchSpanProcessorFactory::Create(std::move(os_exporter), options);
        processors.push_back(std::move(batch_processor));
      } else {
	auto simple_processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(os_exporter));
	processors.push_back(std::move(simple_processor));
      }
    }
    if (otlp_exporter) {
      otlp::OtlpGrpcExporterOptions opts;
      opts.use_ssl_credentials = false;
      opts.endpoint = std::move(endpoint);
      auto ot_exporter  = otlp::OtlpGrpcExporterFactory::Create(opts);
      if (batch_processor) {
        trace_sdk::BatchSpanProcessorOptions options{};
        options.max_queue_size = 25;
        options.schedule_delay_millis = std::chrono::milliseconds(5000);
        options.max_export_batch_size = 10;
        auto batch_processor = trace_sdk::BatchSpanProcessorFactory::Create(std::move(ot_exporter), options);
        processors.push_back(std::move(batch_processor));
      } else {
	auto simple_processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(ot_exporter));
	processors.push_back(std::move(simple_processor));
      }
    }

    auto resource_attributes = resource_sdk::ResourceAttributes {
        {
          "service.name", std::move(service_name)
        }
    };
    auto resource = resource_sdk::Resource::Create(resource_attributes);

    //TODO(thatsdone): create NULL provider and use AddProcessor()s
    std::shared_ptr<trace::TracerProvider> provider =
      trace_sdk::TracerProviderFactory::Create(std::move(processors),
					       resource);
    trace::Provider::SetTracerProvider(provider);
    //
    auto tracer = provider->GetTracer("otetest1", OPENTELEMETRY_SDK_VERSION);
    //
    //main span
    auto span_main = tracer->StartSpan("main");
    cout << "span_main" << endl;
    span_main->SetAttribute("attribute_key1", "attribute_value1");

    //child span
    //do context propagation
    trace::StartSpanOptions span_options;
    span_options.parent = span_main->GetContext();
    auto span_child1 = tracer->StartSpan("child1", span_options);
    span_child1->SetAttribute("attribute_key2", "attribute_value2");

    cout << "span_child1" << endl;

    common::NoopKeyValueIterable links;
    //Note(thatsdone): AddLink() requires ABI Version 2
    //use -DOPENTELEMETRY_ABI_VERSION_NO=2
    auto span_child2 = tracer->StartSpan("child2");
    span_child2->AddLink(span_main->GetContext(), links);

    span_child1->End();
    //child span: end

    span_main->End();
    //main span: end

    return 0;
}
