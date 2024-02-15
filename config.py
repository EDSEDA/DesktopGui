from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_HOST: str = 'localhost'
    RABBITMQ_PORT: int = 5672  # порт по умолчанию для RabbitMQ
    RABBITMQ_USER: str = 'myuser'
    RABBITMQ_PASSWORD: str = 'mypassword'

    QUEUE_NAME: str = 'my_queue'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
