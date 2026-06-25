import requests


PROMETHEUS = "http://localhost:9090"


def get_metric(query):
    r = requests.get(
        f"{PROMETHEUS}/api/v1/query",
        params={"query": query},
    )
    return r.json()


def check_p95_latency():
    query = 'histogram_quantile(0.95, http_request_duration_seconds)'
    data = get_metric(query)

    value = float(data["data"]["result"][0]["value"][1])

    assert value < 0.3, f"P95 too high: {value}"


def check_error_rate():
    query = 'rate(http_requests_total{status=~"5.."}[5m])'
    data = get_metric(query)

    value = float(data["data"]["result"][0]["value"][1])

    assert value < 0.01, f"Error rate too high: {value}"


def check_kafka_lag():
    query = 'kafka_consumer_lag'
    data = get_metric(query)

    value = float(data["data"]["result"][0]["value"][1])

    assert value < 1000, f"Kafka lag too high: {value}"
