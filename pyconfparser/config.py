from abc import ABC, abstractmethod
from os import path
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class Config(ABC):
    conf_type: str

    ERROR_CONF_TYPE_NOT_DEFINED: str = "Can't instantiate {} class without conf_type attribute defined"
    ERROR_PATH_DOES_NOT_EXIST: str = "The given path {} doesn't exist."

    def __init_subclass__(cls, **kwargs: dict[str, Any]) -> None:
        """Force inheritant classes to have conf_type class variable."""
        if not hasattr(cls, "conf_type"):
            raise NotImplementedError(cls.ERROR_CONF_TYPE_NOT_DEFINED.format(cls.__name__))

        return super().__init_subclass__(**kwargs)

    @classmethod
    def get_allowed_types(cls) -> dict[str, "Config"]:
        """Builds a dict of supported conf types extensions.

        Returns:
            dict[str, Conf]: dict with type and allowed conf object
        """
        subclasses = cls.__subclasses__()
        search_attribute = "conf_type"
        allowed_types = {}
        for subclass in subclasses:
            if hasattr(subclass, search_attribute):
                allowed_types[getattr(subclass, search_attribute)] = subclass()
        return allowed_types

    def __init__(self, conf_path: None | str = None):
        abs_path: str | None = path.abspath(conf_path) if conf_path is not None else None
        self._path: str | None = abs_path

    @property
    def path(self) -> str | None:
        """Absolute path of the passed conf file

        Returns:
            str | None: Returns the absolute path of the passed conf file,
            none if the conf file path its not set.
        """
        return self._path

    @path.setter
    def path(self, new_path: str) -> None:
        """Sets a new absolute path for a Conf object"

        Args:
            new_path (str): The new absolute path where the conf file is located.

        Raises:
            ValueError: In case the new path given doesn't exist.
        """
        if not Path(new_path).exists():
            raise ValueError(self.ERROR_PATH_DOES_NOT_EXIST.format(new_path))
        self._path = path.abspath(new_path)

    @abstractmethod
    def ingest_conf(self, schema: None | BaseModel = None) -> "Config":
        """Ingests and makes every field of the conf file an object attribute.
        Args:
            schema (None | BaseModel, optional): A pydantic class to validate that the content
            of a config file follows a given schema.
            Defaults to None.

        Returns:
            Conf: The object with every field in the JSON file as an attribute.
        """
        pass
