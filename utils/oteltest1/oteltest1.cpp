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

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include "opentelemetry/exporters/otlp/otlp_grpc_exporter_factory.h"
#include "opentelemetry/sdk/trace/processor.h"
#include "opentelemetry/sdk/trace/simple_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"
#include "opentelemetry/trace/provider.h"
#include "opentelemetry/sdk/resource/resource.h"
namespace trace     = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace otlp = opentelemetry::exporter::otlp;
namespace resource_sdk  = opentelemetry::sdk::resource;

int main(int argc, char **argv)
{
    po::options_description desc("oteltest1 options");
    desc.add_options()
      ("help", "print help message")
      ("exporter", po::value<std::string>()->default_value("localhost:4317"),
       "OTEL/gRPC exporeter endpoint.")
      ("service_name", po::value<std::string>()->default_value("otetest1"),
       "service_name")
      ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);
    if (vm.count("exporter")) {
      cout << vm["exporter"].as<std::string>() << std::endl;
    }

    otlp::OtlpGrpcExporterOptions opts;
    opts.use_ssl_credentials = false;
    opts.endpoint = vm["service_name"].as<std::string>();
    auto exporter  = otlp::OtlpGrpcExporterFactory::Create(opts);
    auto processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
    auto resource_attributes = resource_sdk::ResourceAttributes
      {
        {"service.name", vm["service_name"].as<std::string>()}
      };
    auto resource = resource_sdk::Resource::Create(resource_attributes);
    auto received_attributes = resource.GetAttributes();

    std::shared_ptr<trace::TracerProvider> provider =
      trace_sdk::TracerProviderFactory::Create(std::move(processor),
					       resource);
    trace::Provider::SetTracerProvider(provider);
    auto tracer = provider->GetTracer("otetest1", "1.0.0");
    auto span = tracer->StartSpan("main");

    cout << "Hello World";

    return 0;
}


