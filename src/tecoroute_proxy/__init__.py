"""TecoRoute Proxy.

Example of synchronous run:

.. code-block:: python

    from tecoroute_proxy import ProxyServer

    server = ProxyServer(port=8080)
    server.run()

Example of asynchronous run:

.. code-block:: python

    from asyncio import run

    from tecoroute_proxy import ProxyServer

    server = ProxyServer(port=8080)
    run(server.run_async())

Example of asynchronous server startup:

.. code-block:: python

    from asyncio import ensure_future, get_event_loop

    from tecoroute_proxy import ProxyServer

    async def main():
        server = ProxyServer(port=8080)
        await server.start()

    ensure_future(main())
    get_event_loop().run_forever()
"""
from ._cli import cli
from ._request import ProxyRequest
from ._server import ProxyServer

__all__ = ["ProxyServer", "ProxyRequest", "cli"]
