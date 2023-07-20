from dotenv import dotenv_values


class Settings:
    def __init__(self):
        self.ENV_PARAMETERS = dotenv_values()

    def get_value(self, key):
        return self.ENV_PARAMETERS.get(key, None)

    @property
    def mongodb_user(self):
        return self.get_value("MONGODB_USER")

    @property
    def mongodb_password(self):
        return self.get_value("MONGODB_PASSWORD")

    @property
    def mongodb_host(self):
        return self.get_value("MONGODB_HOST")

    @property
    def mongodb_db(self):
        return self.get_value("MONGODB_DB")

    @property
    def mongodb_port(self):
        return self.get_value("MONGODB_PORT")


settings = Settings()
