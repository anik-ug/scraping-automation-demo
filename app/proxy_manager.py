from dataclasses import dataclass
from itertools import cycle


@dataclass(frozen=True)
class ProxyEndpoint:
    name: str
    server: str


class ProxyManager:
    """
    Safe demo abstraction.

    In a production system, this component could obtain permitted proxy
    endpoints from an approved provider. Credentials should be supplied
    through environment variables/secrets, never committed to source.
    """

    def __init__(self):
        self._proxies = [
            ProxyEndpoint("proxy-demo-1", "DIRECT"),
            ProxyEndpoint("proxy-demo-2", "DIRECT"),
            ProxyEndpoint("proxy-demo-3", "DIRECT"),
        ]
        self._cycle = cycle(self._proxies)

    def next_proxy(self) -> ProxyEndpoint:
        return next(self._cycle)
