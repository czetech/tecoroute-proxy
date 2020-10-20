# Tecoroute Proxy

**tecoroute-proxy** is a proxy server to Tecoroute service.

## Usage

Usage example:

```python
from tecoroute_proxy import Proxy

if __name__ == '__main__':
    proxy = Proxy()
    print(proxy.client_name)
    proxy.start()
    get_event_loop().run_forever()
```
