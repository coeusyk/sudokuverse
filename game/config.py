import toml
import os

from game.core.constants import NUM_OF_DIFFICULTIES, BASE_DIR


# Messages for exceptions that will be raised manually:
class ErrorMessages:
    def __init__(self, context: str):
        self.context = context
        self.error_msgs: dict[str, dict] = toml.load(os.path.join(BASE_DIR, "instance", "error_messages.toml"))

        self.param_validation(self.context, self.error_msgs, "context")  # Validating the entered context

    def get_error_message(self, inner_context: str, msg_choice: str):
        errors: dict[str, dict] = self.error_msgs[self.context][inner_context]
        self.param_validation(msg_choice, errors, "msg_choice")

        return errors[msg_choice]

    def param_validation(self, value: str, collection: dict[str, dict], parameter: str):
        if (parameter == "context") or (parameter == "msg_choice"):
            errors: dict[str, str] = self.error_msgs["ErrorMessages"][parameter]

        else:
            msg = "invalid parameter: use \'context\' or \'msg_choice\' only"
            raise ValueError(msg)

        type_key, value_key = "INVALID_TYPE", "INVALID_VALUE"

        if not isinstance(value, str):
            raise TypeError(errors[type_key])

        elif value not in collection.keys():
            raise ValueError(errors[value_key])


# Getting all environment variables required for the app:
class Config:
    def __init__(self, num_of_difficulties: int = 3, flask_env: str = "dev"):
        self.flask_env = flask_env

        config_errors_handle = ErrorMessages("Config")  # Error message handler for config
        const_errors_handle = ErrorMessages("Constants")  # Error message handler for constants

        env_error = config_errors_handle.get_error_message("flask_env", "INVALID_VALUE")
        if self.flask_env not in ["dev", "prod"]:
            raise ValueError(env_error)

        num_of_diff_error = const_errors_handle.get_error_message("num_of_difficulties", "INVALID_VALUE")
        if num_of_difficulties != NUM_OF_DIFFICULTIES:
            raise ValueError(num_of_diff_error)

        self.config_file: dict[str, dict] = toml.load(os.path.join(BASE_DIR, "instance", "config.toml"))

    def get_database_uri(self):
        db_info: dict[str, str] = self.config_file["flask_env"][self.flask_env]

        user = db_info["user"]
        password = db_info["password"]
        host = db_info["host"]
        port = db_info["port"]
        db = db_info["db"]

        SQL_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

        return SQL_DATABASE_URI
