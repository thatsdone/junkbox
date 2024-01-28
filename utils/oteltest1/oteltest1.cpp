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
 */
#include <iostream>
#include <vector>
#include <typeinfo>
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
//
#include "opentelemetry/context/propagation/text_map_propagator.h"
//#include "opentelemetry/context/propagation/global_propagator.h"
#include "opentelemetry/trace/propagation/http_trace_context.h"
#include "opentelemetry/baggage/propagation/baggage_propagator.h"
#include "opentelemetry/baggage/baggage_context.h"


namespace trace     = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace otlp = opentelemetry::exporter::otlp;
namespace trace_exporter = opentelemetry::exporter::trace;
namespace resource_sdk  = opentelemetry::sdk::resource;
namespace common  = opentelemetry::common;
namespace context  = opentelemetry::context;
namespace nostd = opentelemetry::nostd;

std::unique_ptr<trace_sdk::SpanProcessor>
get_processor(std::unique_ptr<trace_sdk::SpanExporter> exporter, bool batch)
{
  std::unique_ptr<trace_sdk::SpanProcessor> processor = nullptr;

  if (batch) {
    trace_sdk::BatchSpanProcessorOptions options{};
    options.max_queue_size = 25;
    options.schedule_delay_millis = std::chrono::milliseconds(5000);
    options.max_export_batch_size = 10;
    processor = trace_sdk::BatchSpanProcessorFactory::Create(std::move(exporter), options);
    ;
  } else {
    processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
  }
  return processor;
}


int main(int argc, char **argv)
{
    std::string endpoint = "localhost:4317";
    std::string service_name = "oteltest1";
    bool console_exporter = false;
    bool otlp_exporter = false;
    bool use_batch = false;

    const option longopts[] = {
      {"endpoint", required_argument, nullptr  , 'e'},
      {"service_name", required_argument, nullptr, 'S'},
      {"console", optional_argument, nullptr, 'C'},
      {"otlp", optional_argument, nullptr, 'o'},
      {"use_batch", optional_argument, nullptr, 'B'}
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
        use_batch = true;
        break;
      }
    }

    // prepare span processors with appropriate exporter
    std::vector<std::unique_ptr<trace_sdk::SpanProcessor>> processors;
    std::unique_ptr<trace_sdk::SpanProcessor> processor = nullptr;
    std::unique_ptr<trace_sdk::SpanExporter> exporter = nullptr;

    if (console_exporter) {
      exporter = trace_exporter::OStreamSpanExporterFactory::Create();
      processor = get_processor(std::move(exporter), use_batch);
      processors.push_back(std::move(processor));
    }
    if (otlp_exporter) {
      otlp::OtlpGrpcExporterOptions opts;
      opts.use_ssl_credentials = false;
      opts.endpoint = std::move(endpoint);
      exporter = otlp::OtlpGrpcExporterFactory::Create(opts);
      processor = get_processor(std::move(exporter), use_batch);
      processors.push_back(std::move(processor));
    }

    // prepare resource with service.name
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

    //remote context propagation(using Baggage)
    std::string header = "traceparent=00-0f9da3bc644903c4e4914e75e66a47e0-05eb0528645163a5-01";
    auto baggage = opentelemetry::baggage::Baggage::FromHeader(header);
    std::string value;
    baggage->GetValue("traceparent", value);
    cout << "traceparent: " + value << endl;


    //child span(1)
    //do context propagation
    trace::StartSpanOptions span_options;
    span_options.parent = span_main->GetContext();
    auto span_child1 = tracer->StartSpan("child1", std::move(span_options));
    span_child1->SetAttribute("attribute_key2", "attribute_value2");

    cout << "span_child1" << endl;

    //child span(1)
    common::NoopKeyValueIterable links;
    //Note(thatsdone): AddLink() requires ABI Version 2
    //use -DOPENTELEMETRY_ABI_VERSION_NO=2
    auto span_child2 = tracer->StartSpan("child2");
    //use Link, not context propagation. This should be an independent trace
    //decoupled from main_span.
    span_child2->AddLink(span_main->GetContext(), links);
    cout << "span_child2" << endl;

    span_child2->End();
    //child span(2): end
    
    span_child1->End();
    //child span(1): end

    span_main->End();
    //main span: end

    return 0;
}
