import toml


# Messages for exceptions that will be raised manually:
class ErrorMessages:
    def __init__(self, context: str):
        self.context = context
        self.error_msgs: dict[str, dict] = toml.load("instance/error_messages.toml")
        
        self.param_validation(self.context, self.error_msgs, "context")  # Validating the entered context


    def get_error_message(self, inner_context: str, msg_choice: str):
        errors: dict[str, str] = self.error_msgs[self.context][inner_context]
        self.param_validation(msg_choice, errors, "msg_choice")
        
        return errors[msg_choice]
    

    def param_validation(self, value: str, collection: dict[str, dict], parameter: str):
        if (parameter == "context") or (parameter == "msg_choice"):
            errors: dict[str, str] = self.error_msgs["ErrorMessages"][parameter]

        else:
            msg = "invalid parameter: use \'context\' or \'msg_choice\' only"
            raise ValueError(msg)


        type_key, value_key = "INVALID_TYPE", "INVALID_VALUE"
        if type(value) != str:
            raise TypeError(errors[type_key])

        elif value not in collection.keys():
            raise ValueError(errors[value_key])


# Getting all environment variables required for the app:
class Config:
    def __init__(self, flask_env: str = "dev"):
        self.flask_env = flask_env

        errors_handle = ErrorMessages("Config")
        env_error = errors_handle.get_error_message("flask_env", "INVALID_VALUE")
        if (self.flask_env != "dev") and (self.flask_env != "prod"):
            raise ValueError(env_error)

        self.config_file: dict[str, dict] = toml.load("instance/config.toml")


    def get_database_uri(self):
        db_info: dict[str, str] = self.config_file["flask_env"][self.flask_env]

        user = db_info["user"]; password = db_info["password"]
        host = db_info["host"]; port = db_info["port"]
        db = db_info["db"]

        SQL_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

        return SQL_DATABASE_URI
