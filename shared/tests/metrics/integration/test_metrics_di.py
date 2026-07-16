"""
DI integration tests.
"""

from metrics import Metrics



class Container:


    def __init__(self):

        self._items = {}



    def register(
        self,
        contract,
        instance,
    ):

        self._items[
            contract
        ] = instance



    def resolve(
        self,
        contract,
    ):

        return self._items[
            contract
        ]



def test_metrics_singleton_lifecycle():


    container = Container()


    metrics = Metrics()


    container.register(
        Metrics,
        metrics,
    )


    resolved = container.resolve(
        Metrics
    )


    assert resolved is metrics
