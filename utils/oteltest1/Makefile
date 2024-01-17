all:
	g++  oteltest1.cpp \
	-DOPENTELEMETRY_ABI_VERSION_NO=2 \
	-g \
	-lopentelemetry_exporter_otlp_grpc \
	-lopentelemetry_exporter_ostream_span \
	-lopentelemetry_trace \
	-lopentelemetry_resources \
	-o oteltest1
