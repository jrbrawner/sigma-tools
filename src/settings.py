from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URI: str 
    
    POSTGRES_SERVER: str 
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    ENVIRONMENT: str
    ES_API_KEY: str
    ES_URL: str


    class Config:
        env_file = ".env"


settings = Settings()