# TecoRoute Proxy

TecoRoute Proxy is a reverse proxy server that allows easy authentication to the
[TecoRoute] service using a simple POST request. It also saves the credentials
and automatically logs the user in when the TecoRoute session expires.

## How it works

The server has one control endpoint (`/TR_PROXY` by default) that is used
to log in and log out of the user from the proxy. All other requests are proxied
to TecoRoute. The proxy session is stored only in the user's session cookies, so
the server is completely stateless and no database is required.

The control endpoint accepts `POST` requests with
`application/x-www-form-urlencoded` content type (HTML form).

### Log the user in

The user logs in with the following data:

| Name       | Value                |
| ---------- | -------------------- |
| `action`   | `login`              |
| `username` | _TecoRoute username_ |
| `password` | _TecoRoute password_ |
| `plc`      | _TecoRoute PLC_      |

An example of a HTML form that logs the user in:

```html
<form method="post" action="https://tecoroute-proxy.cze.tech/TR_PROXY">
  <button name="action" value="login">Open PLC</button>
  <input type="hidden" name="username" value="BroukPytlik" />
  <input type="hidden" name="password" value="ferda1" />
  <input type="hidden" name="plc" value="AB_1234" />
</form>
```

### Log the user out

The user logs out with the following data:

| Name     | Value    |
| -------- | -------- |
| `action` | `logout` |

An example of a HTML form that logs the user out:

```html
<form method="post" action="https://tecoroute-proxy.cze.tech/TR_PROXY">
  <button name="action" value="logout">Logout from TecoRoute</button>
</form>
```

Logging out will try to log the user out from TecoRoute and delete the login
data from the user's cookies.

## Usage options

TecoRoute Proxy can be used as a service, standalone application or as a Python
library.

### Use as a service

Server is deployed at <https://tecoroute-proxy.cze.tech>. The control URL is:

    https://tecoroute-proxy.cze.tech/TR_PROXY

Feel free to use the service for testing or simple production purposes.

### Install from [PyPI]

Requirements:

- [Python] (version 3.8 or later)
- [pip] or another package installer for Python

Installation using pip is done with:

```shell
pip install tecoroute-proxy
```

The server starts with:

```shell
tecoroute-proxy
```

On an unprivileged port (e.g. 8080), the server starts with:

```shell
tecoroute-proxy -p 8080
```

For all options, run `tecoroute-proxy --help`.

It is possible to use the package as a Python library and run the server
synchronously or asynchronously in the event loop. An example of usage:

```python
from logging import INFO, basicConfig

from tecoroute_proxy import ProxyServer

basicConfig(level=INFO)
server = ProxyServer(port=8080)
server.run()
```

See full documentation at <https://tecoroute-proxy.readthedocs.io>.

### Run from Docker Hub

Run the image from Docker Hub:

```shell
docker run -p 80:80 czetech/tecoroute-proxy
```

### Install to Kubernetes using Helm

Setup Helm repository:

```shell
helm repo add czetech https://charts.cze.tech/
```

Install Helm chart:

```shell
helm install tecoroute-proxy czetech/tecoroute-proxy \
  --set ingress.enabled=true \
  --set ingress.hosts[0]=<ingress-host>
```

see the [chart] for more options.

## Source code

The source code is available at <https://github.com/czetech/tecoroute-proxy>.

[chart]: https://github.com/czetech/tecoroute-proxy/tree/main/chart
[pip]: https://pip.pypa.io/en/stable/installation/
[pypi]: https://pypi.org/project/tecoroute-proxy/
[python]: https://www.python.org/downloads/
[tecoroute]: https://route.tecomat.com/TR_LOGIN.XML
