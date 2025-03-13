from json import dumps
from pathlib import Path

import pytest
from json_config import JsonConfig
from pydantic import BaseModel


class ConfigurationSchema(BaseModel):
    PASSCODE: str
    ENDPOINTS: dict[str, str]


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Path:
    """Creates a temporary JSON file with test data"""
    test_file: Path = tmp_path / "test.json"
    test_data: dict = {
        "PASSCODE": "some-content",
        "ENDPOINTS": {"ENDPOINT1": "http://your-endpoint-1.com", "ENDPOINT2": "http://your-endpoint-2.com"},
    }
    test_file.write_text(dumps(test_data))
    return test_file


@pytest.fixture
def json_config() -> JsonConfig:
    """Creates a JsonConfig instance for testing"""
    return JsonConfig()


def test_json_config_type() -> None:
    """Test that JsonConfig has correct conf_type"""
    assert JsonConfig.conf_type == ".json"


def test_ingest_conf_without_path(json_config: JsonConfig) -> None:
    """Test ingest_conf raises error when path is not set"""
    with pytest.raises(ValueError) as exc_info:
        json_config.ingest_conf()
    assert str(exc_info.value) == JsonConfig.ERROR_PATH_NOT_SET


def test_ingest_conf_with_schema_instance(json_config: JsonConfig, temp_json_file: Path) -> None:
    """Test ingest_conf raises error when schema instance is passed instead of class"""
    json_config.path = str(temp_json_file)
    schema_instance = ConfigurationSchema(
        PASSCODE="some-content", ENDPOINTS={"ENDPOINT1": "http://your-endpoint-1.com"}
    )

    with pytest.raises(ValueError) as exc_info:
        json_config.ingest_conf(schema_instance)
    assert str(exc_info.value) == JsonConfig.ERROR_INVALID_SCHEMA


def test_ingest_conf_with_invalid_schema(json_config: JsonConfig, tmp_path: Path) -> None:
    """Test ingest_conf with invalid JSON against schema"""
    test_file: Path = tmp_path / "invalid.json"
    invalid_data: dict = {
        "PASS": "some-content",
        "ENDPOINTS": ["http://your-endpoint-1.com", "http://your-endpoint-2.com"],  # a list instead of a dict
    }
    test_file.write_text(dumps(invalid_data))
    json_config.path = str(test_file)

    with pytest.raises(ValueError):
        json_config.ingest_conf(ConfigurationSchema)


def test_ingest_conf_with_valid_schema(json_config: JsonConfig, temp_json_file: Path) -> None:
    """Test ingest_conf with valid schema class"""
    json_config.path = str(temp_json_file)
    result = json_config.ingest_conf(ConfigurationSchema)

    assert isinstance(result, JsonConfig)
    assert hasattr(result, "passcode")
    assert hasattr(result, "endpoints")
    assert result.passcode == "some-content"
    assert isinstance(result.endpoints, dict)
    assert all(endpoint in result.endpoints for endpoint in ["ENDPOINT1", "ENDPOINT2"])
    assert result.endpoints["ENDPOINT1"] == "http://your-endpoint-1.com"
    assert result.endpoints["ENDPOINT2"] == "http://your-endpoint-2.com"


def test_ingest_conf_without_schema(json_config: JsonConfig, temp_json_file: Path) -> None:
    """Test ingest_conf without schema validation"""
    json_config.path = str(temp_json_file)
    result = json_config.ingest_conf()

    assert isinstance(result, JsonConfig)
    assert hasattr(result, "passcode")
    assert hasattr(result, "endpoints")
    assert result.passcode == "some-content"
    assert isinstance(result.endpoints, dict)
    assert all(endpoint in result.endpoints for endpoint in ["ENDPOINT1", "ENDPOINT2"])
    assert result.endpoints["ENDPOINT1"] == "http://your-endpoint-1.com"
    assert result.endpoints["ENDPOINT2"] == "http://your-endpoint-2.com"
