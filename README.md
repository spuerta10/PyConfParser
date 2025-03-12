# PyConfParser
PyConfParser is a secure and flexible Python library for parsing, validating, and managing configuration files.

## Installation
You can install this library via pip:

```shell
pip install git+https://github.com/spuerta10/PyConfParser.git
```

Or install it via [uv](https://docs.astral.sh/uv/):
```shell
uv add git+https://github.com/spuerta10/PyConfParser.git
```

## Usage
Here is a quick example of how to use this library:

```json
{
    "PASS": "some-content",
    "ENDPOINTS": {
        "ENDPOINT1": "http://your-endpoint-1.com",
        "ENDPOINT2": "http://your-endpoint-2.com"
    }
}
```
*configurations.json*

```python
from pyconfparser import ConfigFactory

configurations_path: str = "/path/to/configurations.json"  # the path can be relative or absolute
configurations = ConfigFactory.get_conf(configurations_path)

configurations.api_key  # to obtain 'your-api-key'
configurations.enpoints.endpoint1  # to obtain 'http://your-endpoint-1.com'
configurations.enpoints.endpoint2  # to obtain 'http://your-endpoint-2.com'
```
