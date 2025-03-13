import json

from config import Config
from pydantic import BaseModel


class JsonConfig(Config):
    conf_type = ".json"

    ERROR_PATH_NOT_SET = "The path is not set yet!"
    ERROR_INVALID_SCHEMA = "Please pass the schema class, not an instance of the class."

    def __init__(self, conf_path: None | str = None):
        """Calls super to check path existance and get the absolute path of JSON config file.

        Args:
            conf_path (None | str, optional): The absolute or relative path to JSON config file.
            Defaults to None.
        """
        super().__init__(conf_path)

    # @override
    def ingest_conf(self, schema: None | BaseModel = None) -> "JsonConfig":
        """Ingests and makes every field of the JSON file an object attribute.
        Args:
            schema (None | BaseModel, optional): A pydantic class to validate that
            the content of a config file follows a given schema.
            Defaults to None.

        Raises:
            ValueError: In case the path is not set yet (is None).
            ValueError: In case an instance of a class is passed instead of the class as is.

        Returns:
            JsonConf: The object with every field in the JSON file as an attribute.
        """
        if self._path is None:
            raise ValueError(self.ERROR_PATH_NOT_SET)

        with open(self._path) as conf:
            json_content: dict = json.load(conf)

        if schema is not None:
            if not isinstance(schema, type):
                raise ValueError(self.ERROR_INVALID_SCHEMA)
            schema(**json_content)  # validate that the JSON has the schema specified

        for key, value in json_content.items():
            setattr(self, key.lower(), value)

        return self
