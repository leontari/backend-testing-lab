"""Ramp-up scenario."""
from locust import LoadTestShape


class RampUpShape(LoadTestShape):

    def tick(self):
        run_time = self.get_run_time()

        if run_time < 60:
            return (10, 2)
        elif run_time < 120:
            return (50, 5)
        elif run_time < 180:
            return (100, 10)
        else:
            return None
