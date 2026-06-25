import subprocess
import time
import requests
import pytest


DOCKER_COMPOSE = "docker-compose up -d"


def wait_http(url, timeout=60):
    start = time.time()

    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(2)

    raise TimeoutError(f"Service not ready: {url}")


@pytest.fixture(scope="session", autouse=True)
def system():
    subprocess.run(DOCKER_COMPOSE, shell=True, check=True)

    wait_http("http://localhost:8000/docs")  # gateway

    yield

    subprocess.run("docker-compose down", shell=True)
