from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    db_url: AnyUrl
    host: str
    port: int

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
