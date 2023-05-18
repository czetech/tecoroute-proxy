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
    get,
    middleware,
    post,
    route,
)
from yarl import URL

from ._misc import CONTROL, HOST, HTTP_NAME, ORIGIN, PORT, logger
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
        host: Optional[str] = HOST,
        port: int = PORT,
        control: str = CONTROL,
        origin: str = ORIGIN,
    ) -> None:
        self._host = host
        self._port = port
        self._origin = origin

        server = Application(middlewares=[self._middleware])
        control_path = URL("/").join(URL(control)).path
        server.add_routes(
            [
                get(control_path, self._handler_control_get),
                post(control_path, self._handler_control_post),
                route("*", control_path, self._handler_control),
                route("*", "/{url:.*}", self._handler_all),
            ]
        )
        self._runner = AppRunner(server, access_log=None)

    @middleware  # type: ignore
    async def _middleware(self, request: Request, handler: Handler) -> StreamResponse:
        response = await handler(request)
        response.headers["Server"] = HTTP_NAME
        return response

    async def _handler_control_get(self, request: Request) -> Response:
        return Response(text="OK")

    async def _handler_control_post(self, request: Request) -> Response:
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
        return HTTPMethodNotAllowed(method=request.method, allowed_methods=("POST",))

    async def _handler_all(self, request: Request) -> Response:
        async with ProxyRequest(request, self._origin) as proxy_request:
            return await proxy_request.response()

    async def start(self) -> None:
        """Start the server asynchronously in the event loop."""
        await self._runner.setup()
        await TCPSite(self._runner, self._host, self._port).start()
        logger.info(f"The server is running on {self._host or ''}:{self._port}")

    async def stop(self) -> None:
        """Stop the server."""
        await self._runner.cleanup()
        logger.info("The server stopped")
