from abc import ABC, abstractmethod
from pathlib import Path
from os import path

from pydantic import BaseModel


class Config(ABC):
    
    
    conf_type: str
    

    @property
    @abstractmethod
    def conf_type(cls) -> None:
        """Force inheritant classes to have conf_type class variable.
        """
        pass


    @classmethod
    def get_allowed_types(cls) -> dict[str, 'Config']:
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
    

    def __init__(self, conf_path: None | str):
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
            raise ValueError(f"The given path {new_path} doesn't exist.")
        self._path = path.abspath(new_path)


    @abstractmethod
    def ingest_conf(self, schema: None | BaseModel = None) -> 'Config':
        """Ingests and makes every field of the conf file an object attribute.
        Args:
            schema (None | BaseModel, optional): A pydantic class to validate that the content of a config file follows a given schema. 
            Defaults to None.

        Returns:
            Conf: The object with every field in the JSON file as an attribute.
        """
        pass