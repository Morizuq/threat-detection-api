from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    termii_api_key: str
    termii_sender_id: str
    termii_sms_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()