from os import path
from pathlib import Path

from pydantic import BaseModel

from pyconfparser.config import Config


class ConfigFactory:
    @staticmethod
    def get_conf(conf_path: str, schema: None | BaseModel = None) -> Config:
        """Returns the most appropiate conf object for the filepath given,
        parses the content of the file to a given schema if needed.

        Args:
            conf_path (str): The absolute or relative path to the config file. Defaults to None.
            schema (None | BaseModel, optional): The schema to validate the content of the conf file.
            Defaults to None.

        Returns:
            Conf: The implemented conf object that best fits to the file extension of conf file.
        """

        def init_conf_obj(conf_obj: Config, abs_path: str, schema: None | BaseModel) -> Config:
            """Initializates conf object

            Args:
                conf_obj (Conf): The implemented conf object that best fits to the file extension.
                abs_path (str): The absolute path to the config file. Defaults to None.
                schema (None | BaseModel): The schema to validate the content of the conf file.

            Returns:
                Conf: The initialized conf object.
            """
            conf_obj.path = abs_path
            conf_obj.ingest_conf(schema)
            return conf_obj

        abs_path = path.abspath(conf_path)  # absolute path of conf file
        assert Path(abs_path).exists(), f"The path {conf_path} doesn't exist."

        _, file_extension = path.splitext(conf_path)
        types: dict[str, Config] = Config.get_allowed_types()
        conf_obj: Config | None = types.get(file_extension)

        assert conf_obj is not None, f"{file_extension} type is not yet supported!"
        return init_conf_obj(conf_obj, abs_path, schema)
