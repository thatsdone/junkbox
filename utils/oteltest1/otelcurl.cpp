/**
 * otelcurl.cpp: A tiny exercise program for OpenTelemetry C++
 *
 * License:
 *   Apache License, Version 2.0
 * History:
 * 2024/02/12 v0.1 Initial version
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
#include "opentelemetry/trace/context.h"
//#include "opentelemetry/trace/tracer_context.h"

#include "opentelemetry/context/propagation/global_propagator.h"
#include "opentelemetry/context/propagation/text_map_propagator.h"
#include "opentelemetry/trace/propagation/http_trace_context.h"
#include "opentelemetry/ext/http/client/http_client_factory.h"
#include "opentelemetry/ext/http/common/url_parser.h"
#include "opentelemetry/baggage/propagation/baggage_propagator.h"

namespace trace     = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace otlp = opentelemetry::exporter::otlp;
namespace trace_exporter = opentelemetry::exporter::trace;
namespace resource_sdk  = opentelemetry::sdk::resource;
namespace common  = opentelemetry::common;
namespace context  = opentelemetry::context;
namespace propagation  = opentelemetry::context::propagation;

namespace http_client  = opentelemetry::ext::http::client;

//
#include <curlpp/cURLpp.hpp>
#include <curlpp/Easy.hpp>
#include <curlpp/Options.hpp>

//taken from examples/http/tracer_common.hof opentelemetrcy-cpp
namespace {
template <typename T>
class HttpTextMapCarrier : public opentelemetry::context::propagation::TextMapCarrier
{
public:
  HttpTextMapCarrier(T &headers) : headers_(headers) {}
  HttpTextMapCarrier() = default;
  virtual opentelemetry::nostd::string_view Get(
      opentelemetry::nostd::string_view key) const noexcept override
  {

    //cout << "Get() called." << endl;
    std::string key_to_compare = key.data();
    // Header's first letter seems to be  automatically capitaliazed by our test http-server, so
    // compare accordingly.
    if (key == opentelemetry::trace::propagation::kTraceParent)
    {
      key_to_compare = "Traceparent";
    }
    else if (key == opentelemetry::trace::propagation::kTraceState)
    {
      key_to_compare = "Tracestate";
    }
    auto it = headers_.find(key_to_compare);
    if (it != headers_.end())
    {
      return it->second;
    }
    return "";
  }

  virtual void Set(opentelemetry::nostd::string_view key,
                   opentelemetry::nostd::string_view value) noexcept override
  {
    //debug
    //cout << "Set() called. " + std::string(key) + " / " + std::string(value) << endl;
    headers_.insert(std::pair<std::string, std::string>(std::string(key), std::string(value)));
  }

  T headers_;
};

}

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
    bool enable_otel = true;
    std::string endpoint = "localhost:4317";
    std::string service_name = "oteltest1";
    bool console_exporter = false;
    bool otlp_exporter = false;
    bool use_batch = false;
    std::string url = "";

    const option longopts[] = {
      {"url", required_argument, nullptr},
      {"method", required_argument, nullptr  , 'X'},
      {"data_raw", required_argument, nullptr},
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
    if (argc > optind && argv[optind] != NULL) {
      url = argv[optind];
      for(int i = optind; i < argc; i++) {
        cout << std::string(argv[i]) << endl;
      }
    }
    if (url == "") {
      cout << "Specify URL" << endl;
      exit(255);
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
    propagation::GlobalTextMapPropagator::SetGlobalPropagator(
							      opentelemetry::nostd::shared_ptr<opentelemetry::context::propagation::TextMapPropagator>(new opentelemetry::trace::propagation::HttpTraceContext()));
    auto tracer = provider->GetTracer("otelcurl", OPENTELEMETRY_SDK_VERSION);

    //main span
    auto span_main = tracer->StartSpan("main");
    auto scope = tracer->WithActiveSpan(span_main);

    cout << "span_main" << endl;
    span_main->SetAttribute("attribute_key1", "attribute_value1");

    // trace_id
    auto span_ctx = span_main->GetContext();
    char trace_id_in_span[opentelemetry::trace::TraceId::kSize *2];
    span_ctx.trace_id().ToLowerBase16(trace_id_in_span);
    std::string trace_id_text_in_span{trace_id_in_span, sizeof(trace_id_in_span)};
    cout << trace_id_text_in_span << endl;
    // span_id
    char span_id_in_span[opentelemetry::trace::SpanId::kSize *2];
    span_ctx.span_id().ToLowerBase16(span_id_in_span);
    std::string span_id_text_in_span{span_id_in_span, sizeof(span_id_in_span)};
    cout << span_id_text_in_span << endl;
    // trace_state
    cout << span_ctx.trace_state() << endl;

    auto ctx =  context::RuntimeContext::GetCurrent();
    HttpTextMapCarrier<http_client::Headers> carrier;
    auto prop = context::propagation::GlobalTextMapPropagator::GetGlobalPropagator();
    prop->Inject(carrier, ctx);
    cout << "dump headers... "  << endl;
    for (auto it = carrier.headers_.begin() ; it != carrier.headers_.end(); ++it) {
      cout << (*it).first + " : " + (*it).second << endl;
    }
    cout << "end"  << endl;

    try {
      curlpp::Cleanup cleaner;
      curlpp::Easy request;

      request.setOpt(new curlpp::options::Url(url))
      request.setOpt(new curlpp::options::Verbose(true));
      std::list<std::string> header;
      //header.push_back("Content-Type: application/octet-stream");
      for (auto it = carrier.headers_.begin() ; it != carrier.headers_.end(); ++it) {
        header.push_back((*it).first + ": " + (*it).second);
      }
      request.setOpt(new curlpp::options::HttpHeader(header));
      request.perform();

    } catch (curlpp::LogicError  &e) {
      cout << e.what() << endl;
    } catch (curlpp::RuntimeError  &e) {
      cout << e.what() << endl;
    }

    span_main->End();

    return 0;
}
