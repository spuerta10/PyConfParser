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
### Basic Usage
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
configurations.enpoints["ENDPOINT1"]  # to obtain 'http://your-endpoint-1.com'
configurations.enpoints["ENDPOINT2"]  # to obtain 'http://your-endpoint-2.com'
```

### Using with a Schema
For stricter validation, you can define a schema using `pydantic` to ensure the configuration follows the expected structure.

```python
from pyconfparser import ConfigFactory
from pydantic import BaseModel

class ConfigSchema(BaseModel):
    PASS: str
    ENDPOINTS: dict[str, str]

configurations_path: str = "/path/to/configurations.json"  # the path can be relative or absolute
configurations = ConfigFactory.get_conf(configurations_path, ConfigSchema)

configurations.api_key  # to obtain 'your-api-key'
configurations.enpoints["ENDPOINT1"]  # to obtain 'http://your-endpoint-1.com'
configurations.enpoints["ENDPOINT2"]  # to obtain 'http://your-endpoint-2.com'
```