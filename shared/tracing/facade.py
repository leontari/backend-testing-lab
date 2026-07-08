class Tracing:

    def __init__(
        self,
        propagator,
        factory,
        store,
    ):
        self._propagator = propagator
        self._factory = factory
        self._store = store


    def from_headers(
        self,
        headers: Mapping[str, str],
    ) -> RawTraceCarrier | None:
        """
        Extract trace information.

        Transport-independent.
        """

        return self._propagator.extract(
            headers
        )


    def to_headers(
        self,
        carrier: RawTraceCarrier,
    ) -> dict[str, str]:

        return (
            self._propagator.inject(
                carrier
            )
        )
