from locust import LoadTestShape


class SoakTestShape(LoadTestShape):

    def tick(self):
        return (50, 5)
