from pathlib import Path

import pytest
from pydantic import BaseModel

from pyconfparser.config import Config


class ValidConfiguration(Config):
    conf_type = "valid"

    def ingest_conf(self, _: None | BaseModel = None) -> Config:
        return self


@pytest.fixture
def temp_conf_file(tmp_path: Path) -> Path:
    """Creates a temporary config file for testing.

    Args:
        tmp_path (Path): pytest fixture that provides a temporary directory unique to each test function.

    Returns:
        Path: Path object pointing to the created test file
    """
    test_file: Path = tmp_path / "test.json"
    test_file.touch()
    return test_file


def test_subclass_without_conf_type() -> None:
    with pytest.raises(NotImplementedError):
        """Test that subclass without conf_type raises NotImplementedError"""
        type("InvalidConfiguration", (Config,), {})  # creating the class definition inside the test


def test_subclass_with_conf_type() -> None:
    """Test that subclass with conf_type initializes correctly"""
    config: Config = ValidConfiguration()
    assert config.conf_type == "valid"


def test_get_allowed_types() -> None:
    """Test get_allowed_types returns correct mapping"""
    allowed_types = Config.get_allowed_types()
    assert "valid" in allowed_types
    assert isinstance(allowed_types["valid"], ValidConfiguration)


def test_init_with_path(temp_conf_file: Path) -> None:
    """Test initialization with valid path"""
    config = ValidConfiguration(str(temp_conf_file))
    assert hasattr(config, "_path")
    assert config.path == str(temp_conf_file.absolute())


def test_path_setter_invalid() -> None:
    """Test path setter with invalid path"""
    config = ValidConfiguration()

    with pytest.raises(ValueError) as err_info:
        config.path = "/non/existent/path"
    assert "The given path /non/existent/path doesn't exist." in str(err_info.value)


def test_path_setter_valid(temp_conf_file: Path) -> None:
    """Test path setter with valid path"""
    config = ValidConfiguration()
    config.path = str(temp_conf_file)
    assert config.path == str(temp_conf_file.absolute())


def test_init_with_invalid_path() -> None:
    with pytest.raises(ValueError) as err_info:
        """Test initialization with invalid path"""
        ValidConfiguration("/non/existent/path")
    assert "The given path /non/existent/path doesn't exist." in str(err_info.value)
