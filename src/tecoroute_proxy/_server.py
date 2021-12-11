from asyncio import run, sleep
from typing import Optional

from aiohttp.typedefs import Handler
from aiohttp.web import (
    Application,
    AppRunner,
    HTTPBadRequest,
    HTTPMethodNotAllowed,
    Request,
    Response,
    StreamResponse,
    TCPSite,
    middleware,
    post,
    route,
)
from yarl import URL

from ._misc import (
    CONFIG_CONTROL,
    CONFIG_HOST,
    CONFIG_ORIGIN,
    CONFIG_PORT,
    HTTP_NAME,
    logger,
)
from ._request import ProxyRequest


class ProxyServer:
    """Proxy server.

    :param host: The host to listen on, all interfaces if None.
    :param port: The port to listen on.
    :param control: The control path.
    :param origin: TecoRoute service URL.
    """

    def __init__(
        self,
        host: Optional[str] = CONFIG_HOST,
        port: int = CONFIG_PORT,
        control: str = CONFIG_CONTROL,
        origin: str = CONFIG_ORIGIN,
    ) -> None:
        """:class:`ProxyServer` constructor."""
        self._host = host
        self._port = port
        self._origin = origin

        server = Application(middlewares=[self._middleware])
        control_path = URL("/").join(URL(control)).path
        server.add_routes(
            [
                post(control_path, self._handler_control_post),
                route("*", control_path, self._handler_control),
                route("*", "/{url:.*}", self._handler_all),
            ]
        )
        self._runner = AppRunner(server, access_log=None)

    @middleware  # type: ignore
    async def _middleware(self, request: Request, handler: Handler) -> StreamResponse:
        """Add "Server" header to aiohttp application."""
        response = await handler(request)
        response.headers["Server"] = HTTP_NAME
        return response

    async def _handler_control_post(self, request: Request) -> Response:
        """Control endpoint POST handler."""
        post = await request.post()
        action = post.get("action")
        if action == "login":
            try:
                login = {key: post[key] for key in ("username", "password", "plc")}
            except KeyError as e:
                return HTTPBadRequest(reason=f"Missing {e}.")
            async with ProxyRequest(request, self._origin) as proxy_request:
                return await proxy_request.login(**login)  # type: ignore
        if action == "logout":
            async with ProxyRequest(request, self._origin) as proxy_request:
                return await proxy_request.logout()
        else:
            return HTTPBadRequest(reason="Invalid action.")

    async def _handler_control(self, request: Request) -> Response:
        """Control endpoint handler for other methods."""
        return HTTPMethodNotAllowed(method=request.method, allowed_methods=("POST",))

    async def _handler_all(self, request: Request) -> Response:
        """Catch-all handler."""
        async with ProxyRequest(request, self._origin) as proxy_request:
            return await proxy_request.response()

    async def start(self) -> None:
        """Start the server asynchronously in the event loop."""
        await self._runner.setup()
        await TCPSite(self._runner, self._host, self._port).start()

    async def run_async(self) -> None:
        """Run the server asynchronously."""
        try:
            await self.start()
        except Exception as e:
            logger.error(f"The server could not be started: {e}")
            return
        logger.info(f"The server running on {self._host or ''}:{self._port}")
        while True:
            await sleep(1)

    def run(self) -> None:
        """Run the server synchronously."""
        try:
            run(self.run_async())
        except KeyboardInterrupt:
            logger.info("The server has stopped")
