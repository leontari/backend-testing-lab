from locust import LoadTestShape


class SpikeTestShape(LoadTestShape):

    def tick(self):
        run_time = self.get_run_time()

        if 30 < run_time < 60:
            return (500, 50)
        return (10, 2)
